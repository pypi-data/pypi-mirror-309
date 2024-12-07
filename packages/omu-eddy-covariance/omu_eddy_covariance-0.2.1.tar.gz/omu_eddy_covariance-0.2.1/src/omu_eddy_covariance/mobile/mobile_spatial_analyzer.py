import math
import folium
import numpy as np
import pandas as pd
from dataclasses import dataclass
from logging import getLogger, Formatter, Logger, StreamHandler, DEBUG, INFO
from pathlib import Path


@dataclass
class HotspotData:
    """ホットスポットの情報を保持するデータクラス"""

    angle: float  # 中心からの角度
    ratio: float  # ΔC2H6/ΔCH4の比率
    avg_lat: float  # 平均緯度
    avg_lon: float  # 平均経度
    section: int  # 所属する区画番号
    source: str  # データソース
    type: str  # ホットスポットの種類 ("bio", "gas", or "comb")


@dataclass
class MSAInputConfig:
    """入力ファイルの設定を保持するデータクラス"""

    path: Path | str  # ファイルパス
    delay: int = 0  # 測器の遅れ時間（秒）


class MobileSpatialAnalyzer:
    def __init__(
        self,
        center_lat: float,
        center_lon: float,
        inputs: list[MSAInputConfig] | list[tuple[str | Path, int]],
        num_sections: int,
        ch4_enhance_threshold: float = 0.1,
        correlation_threshold: float = 0.7,
        hotspot_area_meter: float = 30,
        sampling_frequency: float = 1.0,  # サンプリング周波数(Hz)
        window_minutes: float = 5.0,  # 移動窓の大きさ（分）
        logger: Logger | None = None,
        logging_debug: bool = False,
    ):
        """
        測定データ解析クラスの初期化

        Args:
            center_lat: 中心緯度
            center_lon: 中心経度
            inputs: 入力ファイルのリスト
            num_sections: 分割する区画数
            ch4_enhance_threshold: CH4増加の閾値(ppm)
            correlation_threshold: 相関係数の閾値
            hotspot_area_meter (float): ホットスポットの検出に使用するエリアの半径（メートル）。デフォルトは20メートルです。
            sampling_frequency: サンプリング周波数(Hz)
            window_minutes: 移動窓の大きさ（分）
            logger (Logger | None): 使用するロガー。Noneの場合は新しいロガーを作成します。
            logging_debug (bool): ログレベルを"DEBUG"に設定するかどうか。デフォルトはFalseで、Falseの場合はINFO以上のレベルのメッセージが出力されます。
        """
        self.center_lat: float = center_lat
        self.center_lon: float = center_lon
        self.num_sections: int = num_sections
        self.ch4_enhance_threshold: float = ch4_enhance_threshold
        self.correlation_threshold: float = correlation_threshold
        self.hotspot_area_meter: float = hotspot_area_meter
        self.sampling_frequency: float = sampling_frequency

        # セクションの範囲
        self.section_size: float = 360 / num_sections

        # window_sizeをデータポイント数に変換（分→秒→データポイント数）
        self.window_size: int = self.__calculate_window_size(window_minutes)

        # 入力設定の標準化
        self.__input_configs = self.__normalize_inputs(inputs)
        # 複数ファイルのデータを読み込み
        self.__data = self.__load_all_data()
        self.__sections = self.__initialize_sections()

        # ロガー
        log_level: int = INFO
        if logging_debug:
            log_level = DEBUG
        self.logger: Logger = self.__setup_logger(logger, log_level)

    def __setup_logger(self, logger: Logger | None, log_level: int = INFO):
        """
        ロガーを設定します。

        このメソッドは、ロギングの設定を行い、ログメッセージのフォーマットを指定します。
        ログメッセージには、日付、ログレベル、メッセージが含まれます。

        渡されたロガーがNoneまたは不正な場合は、新たにロガーを作成し、標準出力に
        ログメッセージが表示されるようにStreamHandlerを追加します。ロガーのレベルは
        引数で指定されたlog_levelに基づいて設定されます。

        Args:
            logger (Logger | None): 使用するロガー。Noneの場合は新しいロガーを作成します。
            log_level (int): ロガーのログレベル。デフォルトはINFO。

        Returns:
            Logger: 設定されたロガーオブジェクト。
        """
        if logger is not None and isinstance(logger, Logger):
            return logger
        # 渡されたロガーがNoneまたは正しいものでない場合は独自に設定
        logger: Logger = getLogger()
        logger.setLevel(log_level)  # ロガーのレベルを設定
        ch = StreamHandler()
        ch_formatter = Formatter("%(asctime)s - %(levelname)s - %(message)s")
        ch.setFormatter(ch_formatter)  # フォーマッターをハンドラーに設定
        logger.addHandler(ch)  # StreamHandlerの追加
        return logger

    def __calculate_angle(self, lat: float, lon: float) -> float:
        """
        中心からの角度を計算

        Args:
            lat (float): 緯度
            lon (float): 経度

        Returns:
            float: 真北を0°として時計回りの角度（-180°から180°）
        """
        d_lat = lat - self.center_lat
        d_lon = lon - self.center_lon

        # arctanを使用して角度を計算（ラジアン）
        angle_rad = math.atan2(d_lon, d_lat)

        # ラジアンから度に変換（-180から180の範囲）
        angle_deg = math.degrees(angle_rad)
        return angle_deg

    def __calculate_distance(
        self, lat1: float, lon1: float, lat2: float, lon2: float
    ) -> float:
        """
        2点間の距離をメートル単位で計算（Haversine formula）

        Args:
            lat1 (float): 地点1の緯度
            lon1 (float): 地点1の経度
            lat2 (float): 地点2の緯度
            lon2 (float): 地点2の経度

        Returns:
            float: 2点間の距離（メートル）
        """
        R = 6371000  # 地球の半径（メートル）

        # 緯度経度をラジアンに変換
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)

        # 緯度と経度の差分
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        # Haversine formula
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c  # メートル単位での距離

    def __calculate_hotspots_parameters(
        self, df: pd.DataFrame, window_size: int
    ) -> pd.DataFrame:
        """パラメータ計算

        Args:
            df (pd.DataFrame): 入力データフレーム
            window_size (int): 移動窓のサイズ

        Returns:
            pd.DataFrame: 計算されたパラメータを含むデータフレーム
        """
        # 移動平均の計算
        df["ch4_ppm_mv"] = (
            df["ch4_ppm"].rolling(window=window_size, center=True, min_periods=1).mean()
        )

        df["c2h6_ppb_mv"] = (
            df["c2h6_ppb"]
            .rolling(window=window_size, center=True, min_periods=1)
            .mean()
        )

        # 移動相関の計算
        df["ch4_c2h6_correlation"] = (
            df["ch4_ppm"]
            .rolling(window=window_size, min_periods=1)
            .corr(df["c2h6_ppb"])
        )

        # 移動平均からの偏差
        df["ch4_ppm_delta"] = df["ch4_ppm"] - df["ch4_ppm_mv"]
        df["c2h6_ppb_delta"] = df["c2h6_ppb"] - df["c2h6_ppb_mv"]

        # C2H6/CH4の比率計算
        df["c2h6_ch4_ratio"] = df["c2h6_ppb"] / df["ch4_ppm"]

        # デルタ値に基づく比の計算
        ch4_threshold = 0.05  # 閾値
        df["c2h6_ch4_ratio_delta"] = np.where(
            (df["ch4_ppm_delta"].abs() >= ch4_threshold)
            & (df["c2h6_ppb_delta"] >= 0.0),
            df["c2h6_ppb_delta"] / df["ch4_ppm_delta"],
            np.nan,
        )

        return df

    def __calculate_window_size(self, window_minutes: float) -> int:
        """
        時間窓からデータポイント数を計算

        Args:
            window_minutes (float): 時間窓の大きさ（分）

        Returns:
            int: データポイント数
        """
        return int(60 * window_minutes)

    def __detect_hotspots(
        self,
        df: pd.DataFrame,
        ch4_enhance_threshold: float,
        hotspot_areas_meter: float,
    ) -> list[HotspotData]:
        """シンプル化したホットスポット検出

        Args:
            df (pd.DataFrame): 入力データフレーム
            ch4_enhance_threshold (float): CH4増加の閾値
            hotspot_areas_meter (float): ホットスポット間の最小距離（メートル）

        Returns:
            list[HotspotData]: 検出されたホットスポットのリスト
        """
        hotspots: list[HotspotData] = []
        # タイプごとに使用された位置を記録
        used_positions_by_type = {"bio": set(), "gas": set(), "comb": set()}

        # CH4増加量が閾値を超えるデータポイントを抽出
        enhanced_mask = df["ch4_ppm"] - df["ch4_ppm_mv"] > ch4_enhance_threshold

        if enhanced_mask.any():
            # 必要なデータを抽出
            lat = df["latitude"][enhanced_mask]
            lon = df["longitude"][enhanced_mask]
            ratios = df["c2h6_ch4_ratio_delta"][enhanced_mask]

            # デバッグ情報の出力
            self.logger.debug(f"{lat};{lon};{ratios}")

            # 各ポイントに対してホットスポットを作成
            for i in range(len(lat)):
                if pd.notna(ratios.iloc[i]):
                    current_lat = lat.iloc[i]
                    current_lon = lon.iloc[i]

                    # 比率に基づいてタイプを決定
                    if ratios.iloc[i] >= 100:
                        spot_type = "comb"
                    elif ratios.iloc[i] >= 5:
                        spot_type = "gas"
                    else:
                        spot_type = "bio"

                    # 同じタイプのホットスポットとの距離のみをチェック
                    too_close = False
                    for used_lat, used_lon in used_positions_by_type[spot_type]:
                        distance = self.__calculate_distance(
                            current_lat, current_lon, used_lat, used_lon
                        )
                        if distance < hotspot_areas_meter:
                            too_close = True
                            break

                    if too_close:
                        continue

                    angle = self.__calculate_angle(current_lat, current_lon)
                    section = self.__determine_section(angle)

                    hotspots.append(
                        HotspotData(
                            angle=angle,
                            ratio=ratios.iloc[i],
                            avg_lat=current_lat,
                            avg_lon=current_lon,
                            section=section,
                            source=ratios.index[i].strftime("%Y-%m-%d"),
                            type=spot_type,
                        )
                    )

                    # タイプごとに使用した位置を記録
                    used_positions_by_type[spot_type].add((current_lat, current_lon))

        return hotspots

    def __determine_section(self, angle: float) -> int:
        """
        角度から所属する区画を判定

        Args:
            angle (float): 計算された角度

        Returns:
            int: 区画番号
        """
        for section_num, (start, end) in self.__sections.items():
            if start <= angle < end:
                return section_num
        # -180度の場合は最後の区画に含める
        return self.num_sections - 1

    def __initialize_sections(self) -> dict[int, tuple[float, float]]:
        """区画の初期化

        Returns:
            dict[int, tuple[float, float]]: 区画番号とその範囲の辞書
        """
        sections = {}
        for i in range(self.num_sections):
            # -180から180の範囲で区画を設定
            start_angle = -180 + i * self.section_size
            end_angle = -180 + (i + 1) * self.section_size
            sections[i] = (start_angle, end_angle)
        return sections

    def __load_all_data(self) -> dict[str, pd.DataFrame]:
        """全入力ファイルのデータを読み込む

        Returns:
            dict[str, pd.DataFrame]: 読み込まれたデータフレームの辞書
        """
        all_data = {}
        for config in self.__input_configs:
            df = self.__load_data(config)
            source_name = Path(config.path).stem
            all_data[source_name] = df
        return all_data

    def __load_data(self, config: MSAInputConfig) -> pd.DataFrame:
        """
        測定データの読み込みと前処理

        Args:
            config (MSAInputConfig): 入力ファイルの設定

        Returns:
            pd.DataFrame: 読み込んだデータフレーム
        """
        df = pd.read_csv(config.path, na_values=["No Data", "nan"])

        # カラム名の標準化（測器に依存しない汎用的な名前に変更）
        column_mapping = {
            "Time Stamp": "timestamp",
            "CH4 (ppm)": "ch4_ppm",
            "C2H6 (ppb)": "c2h6_ppb",
            "H2O (ppm)": "h2o_ppm",
            "Latitude": "latitude",
            "Longitude": "longitude",
        }
        df = df.rename(columns=column_mapping)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df.set_index("timestamp", inplace=True)

        if config.delay > 0:
            # 遅れ時間の補正
            columns_to_shift = ["ch4_ppm", "c2h6_ppb", "h2o_ppm"]
            shift_periods = -config.delay

            for col in columns_to_shift:
                df[col] = df[col].shift(shift_periods)

            df = df.dropna(subset=columns_to_shift)

        # 水蒸気フィルタリング
        df[df["h2o_ppm"] < 2000] = np.nan
        df.dropna(subset=["ch4_ppm"], inplace=True)

        return df

    def __normalize_inputs(
        self, inputs: list[MSAInputConfig] | list[tuple[str | Path, int]]
    ) -> list[MSAInputConfig]:
        """入力設定を標準化

        Args:
            inputs (list[MSAInputConfig] | list[tuple[str | Path, int]]): 入力設定のリスト

        Returns:
            list[MSAInputConfig]: 標準化された入力設定のリスト
        """
        normalized = []
        for inp in inputs:
            if isinstance(inp, MSAInputConfig):
                normalized.append(inp)
            else:
                path, delay = inp
                # 拡張子の確認
                extension = Path(path).suffix
                if extension not in [".txt", ".csv"]:
                    raise ValueError(f"Unsupported file extension: {extension}")
                normalized.append(MSAInputConfig(path=path, delay=delay))
        return normalized

    def analyze_hotspots(self) -> list[HotspotData]:
        """
        ホットスポットを検出して分析します。

        このメソッドは、クラス初期化時に設定されたwindow_sizeを使用して、
        各データソースに対してホットスポットを検出し、分析結果を返します。

        Returns:
            list[HotspotData]: 検出されたホットスポットのリスト。
            各ホットスポットは、位置、比率、タイプなどの情報を含みます。
        """
        all_hotspots: list[HotspotData] = []

        # 各データソースに対して解析を実行
        for _, df in self.__data.items():
            # パラメータの計算
            df = self.__calculate_hotspots_parameters(df, self.window_size)

            # ホットスポットの検出
            hotspots = self.__detect_hotspots(
                df,
                ch4_enhance_threshold=self.ch4_enhance_threshold,
                hotspot_areas_meter=self.hotspot_area_meter,
            )
            all_hotspots.extend(hotspots)

        return all_hotspots

    def create_hotspots_map(
        self, hotspots: list[HotspotData], output_path: str | Path
    ) -> None:
        """
        ホットスポットの分布を地図上にプロットして保存

        Args:
            hotspots (list[HotspotData]): プロットするホットスポットのリスト
            output_path (str | Path): 保存先のパス
        """
        # 地図の作成
        m = folium.Map(
            location=[self.center_lat, self.center_lon],
            zoom_start=15,
            tiles="OpenStreetMap",
        )

        # ホットスポットの種類ごとに異なる色でプロット
        for spot in hotspots:
            # NaN値チェックを追加
            if math.isnan(spot.avg_lat) or math.isnan(spot.avg_lon):
                continue

            # タイプに応じて色を設定
            if spot.type == "comb":
                color = "green"
            elif spot.type == "gas":
                color = "red"
            else:  # bio
                color = "blue"

            # HTMLタグを含むテキストを適切にフォーマット
            popup_html = f"""
            <div style='font-family: Arial; font-size: 12px;'>
                <b>Type:</b> {spot.type}<br>
                <b>Date:</b> {spot.source}<br>
                <b>Ratio:</b> {spot.ratio:.3f}<br>
                <b>Section:</b> {spot.section}
            </div>
            """

            # ポップアップのサイズを指定
            popup = folium.Popup(
                folium.Html(popup_html, script=True),
                max_width=200,  # 最大幅（ピクセル）
            )

            folium.CircleMarker(
                location=[spot.avg_lat, spot.avg_lon],
                radius=8,
                color=color,
                fill=True,
                popup=popup,
            ).add_to(m)

        # 中心点のマーカー
        folium.Marker(
            [self.center_lat, self.center_lon],
            popup="Center",
            icon=folium.Icon(color="green", icon="info-sign"),
        ).add_to(m)

        # 区画の境界線を描画
        for section in range(self.num_sections):
            start_angle = math.radians(-180 + section * self.section_size)

            # 区画の境界線を描画（3000mの半径で）
            radius_meters = 3000
            R = 6371000  # 地球の半径（メートル）

            # 境界線の座標を計算
            lat1 = self.center_lat
            lon1 = self.center_lon
            lat2 = math.degrees(
                math.asin(
                    math.sin(math.radians(lat1)) * math.cos(radius_meters / R)
                    + math.cos(math.radians(lat1))
                    * math.sin(radius_meters / R)
                    * math.cos(start_angle)
                )
            )
            lon2 = self.center_lon + math.degrees(
                math.atan2(
                    math.sin(start_angle)
                    * math.sin(radius_meters / R)
                    * math.cos(math.radians(lat1)),
                    math.cos(radius_meters / R)
                    - math.sin(math.radians(lat1)) * math.sin(math.radians(lat2)),
                )
            )

            # 境界線を描画
            folium.PolyLine(
                locations=[[lat1, lon1], [lat2, lon2]],
                color="black",
                weight=1,
                opacity=0.5,
            ).add_to(m)

        # 地図を保存
        m.save(str(output_path))
        self.logger.info(f"地図を保存しました: {output_path}")
