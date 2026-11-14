# =========================================================
if section == "🧬 الگوهای تاریخی":
    st.title("🧬 موتور هوشمند الگوهای تاریخی")
    st.caption("مقایسه وضعیت فعلی با نمونه‌های گذشته، سنجش بازده بعدی و آزمون زمانی؛ نه صرفاً امتیازدهی با اندیکاتورهای ثابت")
    st.info(
        "این موتور از تاریخچه CoinGecko استفاده می‌کند: تا ۹۰ روز داده ساعتی تجمیع‌شده و در بازه‌های بلندتر داده روزانه. "
        "گردش ۲۴ساعته فقط پروکسی حجم است و کندل‌ها OHLC رسمی صرافی نیستند. برای جلوگیری از نگاه به آینده، "
        "سه خروجی جدا داریم: تاریخچه خود ارز، نمونه‌های بین‌ارزی، و نزدیک‌ترین الگوهای تاریخی که پس از آن‌ها رشد حداقل ۱۰٪ رخ داده است. تعداد نمونه‌های واقعی هر بخش جدا نمایش داده می‌شود. " 
        "نمونه‌ها فقط وقتی وارد مقایسه می‌شوند که نتیجه ۷ روز بعدشان کامل شده باشد. "
        "آمار مشابه‌ها احتمال کالیبره‌شده یا تضمین رشد نیست؛ بک‌تست نیز فقط روی دارایی‌های فعلاً فهرست‌شده انجام می‌شود و سوگیری بقا را کاملاً حذف نمی‌کند."
    )
    hist_key = secret_or_env("COINGECKO_API_KEY")
    h1, h2, h3 = st.columns(3)
    with h1:
        hist_universe = st.selectbox("تعداد ارزهای اولیه از CoinGecko", [100, 250, 500], index=1, key="hist_pattern_universe")
    with h2:
        hist_assets = st.selectbox("تعداد ارزهای دارای تاریخچه", [20, 30, 40, 60], index=1, key="hist_pattern_assets")
    with h3:
        hist_days = st.selectbox("طول تاریخچه (روز)", [90, 180, 365], index=2, key="hist_pattern_days")
    st.caption(
        "فیلتر پایه: ارزش بازار حداقل ۱۰ میلیون دلار و حجم ۲۴ساعته حداقل ۳۰۰ هزار دلار. "
        "BTC برای محاسبه قدرت نسبی جداگانه اضافه می‌شود. منبع: CoinGecko؛ بدون نیاز به کلید پولی CMC."
    )
    st.caption("ویژگی‌ها از قیمت‌های ساعتی تجمیع‌شده به روزانه، گردش معاملاتی ۲۴ساعته به‌عنوان پروکسی، فشردگی دامنه، کف‌های بالاتر، RSI و قدرت نسبی در برابر BTC ساخته می‌شوند. حجم این منبع، حجم خالص ورود پول یا حجم واقعی کندل نیست؛ داده تاریخی نهنگ‌ها، Funding و Open Interest نیز در این منبع وجود ندارد.")
    st.info("CoinGecko در بازه تا ۹۰ روز معمولاً داده ساعتی و در بازه بلندتر داده روزانه ارائه می‌کند. در هر دو حالت، گردش ۲۴ساعته پروکسی است و داده ورود پول خالص نیست. درخواست ۳۶۵روزه ممکن است با توجه به محدودیت پلن یا نرخ درخواست API رد شود.")
    if st.button("🔬 اجرای مقایسه الگوهای تاریخی و بک‌تست", type="primary", key="run_historical_pattern_engine"):
        with st.spinner(f"در حال دریافت تاریخچه {hist_days}روزه CoinGecko، ساخت بانک نمونه‌ها و اجرای آزمون walk-forward..."):
            try:
                hist_result, hist_meta, hist_backtest = run_historical_pattern_scan(
                    hist_universe, hist_key, max_assets=hist_assets, history_days=hist_days
                )
                st.session_state["historical_pattern_result_v1"] = hist_result
                st.session_state["historical_pattern_meta_v1"] = hist_meta
                st.session_state["historical_pattern_backtest_v1"] = hist_backtest
                st.session_state["historical_pattern_run_time_v1"] = pd.Timestamp.now(tz="UTC").strftime("%Y-%m-%d %H:%M UTC")
            except Exception as exc:
                st.error(f"اجرای موتور تاریخی ناموفق بود: {str(exc)[:500]}")
                if "429" in str(exc):
                    st.warning("محدودیت تعداد درخواست CoinGecko رخ داده است. چند دقیقه صبر کن و دوباره اجرا کن؛ از زدن پیاپی دکمه خودداری کن.")
                elif "403" in str(exc) or "plan" in str(exc).lower() or "subscription" in str(exc).lower():
                    st.warning("CoinGecko دسترسی این درخواست را رد کرده است. وضعیت پلن یا محدودیت IP را بررسی کن؛ این موتور به CMC وابسته نیست.")
    hist_result = st.session_state.get("historical_pattern_result_v1", pd.DataFrame())
    hist_meta = st.session_state.get("historical_pattern_meta_v1", {})
    hist_backtest = st.session_state.get("historical_pattern_backtest_v1", {})
    if isinstance(hist_result, pd.DataFrame) and not hist_result.empty:
        st.caption(
            f"آخرین اجرا: {st.session_state.get('historical_pattern_run_time_v1', '—')} • "
            f"ارزهای دارای تاریخچه: {hist_meta.get('assets_with_history', 0)} • "
            f"طول تاریخچه: {hist_meta.get('history_days_requested', '—')} روز • "
            f"نمونه‌های تاریخی: {hist_meta.get('historical_samples', 0):,} • "
            f"خطاهای دسته‌ای API: {hist_meta.get('errors', 0)} • تاریخ داده: {hist_meta.get('as_of_utc', '—')}"
        )
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("نمونه‌های تاریخی", f"{hist_meta.get('historical_samples', 0):,}")
        k2.metric("دارای تاریخچه", hist_meta.get("assets_with_history", 0))
        k3.metric("تعداد آزمون‌های خارج از نمونه", hist_backtest.get("test_cases", 0))
        k4.metric("سیگنال‌های بک‌تست", hist_backtest.get("signals", 0))
        st.caption("توجه داده‌ای: حجم = میانه گردش ۲۴ساعته CoinGecko (پروکسی)، نه ورود پول خالص؛ سقف/کف روزانه از نمونه‌های ساعتی است، نه کندل رسمی صرافی.")
        st.subheader("🔎 ارزهایی با الگوهای تاریخی مشابه")
        hist_columns = [
            "Coin", "Symbol", "Analog_Match_Count", "Analog_Same_Asset_Count",
            "Analog_Cross_Asset_Count", "Analog_Source_Asset_Count",
            "SameAsset_Analog_Hit_Rate_7d", "SameAsset_Analog_Pump_Rate_7d",
            "CrossAsset_Analog_Hit_Rate_7d", "CrossAsset_Analog_Pump_Rate_7d",
            "Pump_Precedent_Count", "Pump_Precedent_Source_Assets",
            "Pump_Precedent_Median_Distance", "Analog_Hit_Rate_3d", "Analog_Hit_Rate_7d",
            "Analog_Pump_Rate_7d", "Analog_CI_Lower_7d", "Analog_CI_Upper_7d", "Analog_Median_Return_3d",
            "Analog_Median_Return_7d", "Analog_Mean_Return_7d", "Analog_Median_MFE_7d", "Analog_Median_MAE_7d",
            "Analog_Median_Distance", "Analog_Score", "Analog_Status", "ret_1d", "ret_3d", "ret_7d",
            "volume_ratio_3v14", "range_compression_3v14", "higher_low_3v7", "rsi_14",
            "relative_strength_7d", "Last_Completed_Day"
        ]
        hist_columns = [c for c in hist_columns if c in hist_result.columns]
        hist_labels = {
            "Coin": "ارز", "Symbol": "نماد", "Analog_Match_Count": "تعداد نمونه مشابه",
            "Analog_Same_Asset_Count": "نمونه از تاریخچه همین ارز",
            "Analog_Cross_Asset_Count": "تعداد نمونه بین‌ارزی",
            "Analog_Source_Asset_Count": "تعداد ارزهای منبع نمونه‌ها",
            "SameAsset_Analog_Hit_Rate_7d": "نرخ رشد ≥۵٪ در تاریخچه همین ارز (%)",
            "SameAsset_Analog_Pump_Rate_7d": "نرخ پامپ در تاریخچه همین ارز (%)",
            "CrossAsset_Analog_Hit_Rate_7d": "نرخ رشد ≥۵٪ در الگوهای بین‌ارزی (%)",
            "CrossAsset_Analog_Pump_Rate_7d": "نرخ پامپ در الگوهای بین‌ارزی (%)",
            "Pump_Precedent_Count": "تعداد نزدیک‌ترین نمونه‌های منتهی به پامپ",
            "Pump_Precedent_Source_Assets": "تعداد ارزهای دارای نمونه پامپی",
            "Pump_Precedent_Median_Distance": "فاصله میانه تا الگوهای پیش از پامپ",
            "Analog_Hit_Rate_3d": "نرخ رشد ≥۳٪ در ۳روز (%)",
            "Analog_Hit_Rate_7d": "نرخ رشد ≥۵٪ در ۷روز (%)",
            "Analog_Pump_Rate_7d": "نرخ رشد ≥۱۰٪ در ۷روز (%)",
            "Analog_CI_Lower_7d": "حد پایین بازه اطمینان ۷روزه (%)",
            "Analog_CI_Upper_7d": "حد بالای بازه اطمینان ۷روزه (%)",
            "Analog_Median_Return_3d": "میانه بازده ۳روزه (%)",
            "Analog_Median_Return_7d": "میانه بازده ۷روزه (%)",
            "Analog_Mean_Return_7d": "میانگین بازده ۷روزه (%)",
            "Analog_Median_MFE_7d": "میانه بیشترین رشد ۷روزه (%)",
            "Analog_Median_MAE_7d": "میانه بیشترین افت ۷روزه (%)",
            "Analog_Median_Distance": "فاصله آماری نمونه‌ها (کمتر بهتر)",
            "Analog_Score": "امتیاز ترکیبی الگوی تاریخی با وزن بیشتر برای نرخ پامپ",
            "Analog_Status": "نتیجه نمونه‌های مشابه",
            "ret_1d": "بازده ۱روزه فعلی (%)", "ret_3d": "بازده ۳روزه فعلی (%)",
            "ret_7d": "بازده ۷روزه فعلی (%)", "volume_ratio_3v14": "پروکسی گردش ۲۴ساعته: ۳روز / ۱۴روز قبلی",
            "range_compression_3v14": "فشردگی دامنه ۳روز / ۱۴روز قبلی",
            "higher_low_3v7": "تغییر کف ۳روز نسبت به ۷روز قبلی (%)",
            "rsi_14": "RSI 14", "relative_strength_7d": "قدرت نسبی ۷روزه نسبت به BTC (%)",
            "Last_Completed_Day": "آخرین روز کامل‌شده"
        }
