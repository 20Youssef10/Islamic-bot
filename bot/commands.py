import discord
import traceback
import random
from datetime import datetime, timedelta
from services.quran_service import get_random_ayah
from services.audio_service import get_audio
from services.azkar_service import get_zikr
from services.semantic_search import semantic_search
from services.hadith_service import get_random_hadith, HADITH_COLLECTIONS
from services.tafsir_service import get_tafsir, get_surah_info
from services.prayer_times_service import get_prayer_times, get_next_prayer
from services.favorites_service import add_favorite, get_user_favorites, remove_favorite, is_favorite
from services.islamic_knowledge_service import (
    get_random_name_of_allah, get_dua, get_islamic_quiz, 
    get_islamic_quote, get_allah_names_list, ISLAMIC_DUAS
)
from services.tracking_service import (
    track_prayer, get_prayer_stats, track_qada_prayers, get_qada_count,
    mark_qada_completed, track_fasting, get_fasting_stats, track_quran_reading,
    get_quran_reading_stats, get_khatm_progress, track_tasbeeh, get_tasbeeh_stats
)
from services.scheduled_azkar_service import setup_schedule_azkar_command

def setup_commands(bot):

    # ============================================================
    # HELP & INFO (4 commands)
    # ============================================================

    @bot.tree.command(name="help", description="عرض قائمة الأوامر المتاحة")
    async def help_command(interaction: discord.Interaction):
        try:
            embed = discord.Embed(
                title="📖 Islamic Bot - قائمة الأوامر",
                description="**مرحباً بك في البوت الإسلامي الشامل!**\n50+ أمر إسلامي متاح",
                color=discord.Color.green()
            )
            embed.add_field(name="📚 القرآن (10)", value="`/ayah`, `/ayah_audio`, `/surah_info`, `/tafsir`, `/search_semantic`, `/quran_page`, `/quran_juz`, `/verse_by_topic`, `/memorization_tip`, `/quran_challenge`", inline=False)
            embed.add_field(name="📖 الحديث (8)", value="`/hadith`, `/hadith_collection`, `/hadith_40_nawawi`, `/daily_hadith`, `/hadith_search`, `/hadith_explain`, `/hadith_quiz`, `/fortress_muslim`", inline=False)
            embed.add_field(name="🤲 الأذكار (8)", value="`/zikr`, `/tasbeeh`, `/tasbeeh_counter`, `/daily_azkar`, `/dua_situation`, `/masnoon_dua`, `/ruqyah`, `/istikhara`", inline=False)
            embed.add_field(name="🕌 الصلاة (8)", value="`/prayer_times`, `/next_prayer`, `/qibla`, `/prayer_track`, `/qada_track`, `/prayer_stats`, `/mosque_finder`, `/adhan`", inline=False)
            embed.add_field(name="🎓 المعرفة (8)", value="`/names_allah`, `/islamic_quiz`, `/islamic_fact`, `/golden_quote`, `/seerah`, `/fiqh_ruling`, `/islamic_date`, `/ramadan_countdown`", inline=False)
            embed.add_field(name="📊 التتبع (6)", value="`/fasting_track`, `/quran_track`, `/khatm_progress`, `/streaks`, `/islamic_goals`, `/weekly_report`", inline=False)
            embed.add_field(name="⚙️ عام (4)", value="`/bot_info`, `/settings`, `/invite`, `/help`", inline=False)
            embed.set_footer(text="جزاك الله خيراً 🤲")
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message("❌ حدث خطأ", ephemeral=True)

    @bot.tree.command(name="bot_info", description="معلومات عن البوت")
    async def bot_info(interaction: discord.Interaction):
        embed = discord.Embed(title="🤖 معلومات البوت", color=discord.Color.blue())
        embed.add_field(name="الإصدار", value="2.0", inline=True)
        embed.add_field(name="الأوامر", value="50+", inline=True)
        embed.add_field(name="السور", value="114", inline=True)
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="invite", description="دعوة البوت")
    async def invite_bot(interaction: discord.Interaction):
        await interaction.response.send_message("🔗 **دعوة البوت:**\nhttps://discord.com/oauth2/authorize?client_id=1459564811183591686&scope=bot&permissions=2147483647", ephemeral=True)

    @bot.tree.command(name="settings", description="الإعدادات")
    async def settings_cmd(interaction: discord.Interaction):
        await interaction.response.send_message("⚙️ **الإعدادات**\nاستخدم الأوامر لتخصيص البوت", ephemeral=True)

    # ============================================================
    # QURAN (10 commands)
    # ============================================================

    @bot.tree.command(name="ayah", description="آية عشوائية")
    async def ayah(interaction: discord.Interaction):
        try:
            a = get_random_ayah()
            embed = discord.Embed(title=a['ref'], description=a['text'], color=discord.Color.teal())
            embed.set_footer(text=f"آية رقم: {a['id']}")
            await interaction.response.send_message(embed=embed)
        except:
            await interaction.response.send_message("❌ حدث خطأ", ephemeral=True)

    @bot.tree.command(name="ayah_audio", description="آية مع تلاوة")
    async def ayah_audio(interaction: discord.Interaction, reciter: str = "ar.alafasy"):
        try:
            await interaction.response.defer()
            a = get_random_ayah()
            audio = get_audio(a["id"], reciter)
            embed = discord.Embed(title=f"🎧 {a['ref']}", description=a['text'], color=discord.Color.teal())
            await interaction.followup.send(embed=embed, file=discord.File(audio))
        except:
            await interaction.followup.send("❌ حدث خطأ")

    @bot.tree.command(name="surah_info", description="معلومات سورة")
    async def surah_info(interaction: discord.Interaction, surah_number: int):
        if not 1 <= surah_number <= 114:
            await interaction.response.send_message("❌ رقم السورة 1-114", ephemeral=True)
            return
        info = get_surah_info(surah_number)
        embed = discord.Embed(title=f"📖 سورة {info['name']}", color=discord.Color.teal())
        embed.add_field(name="المعنى", value=info['meaning'], inline=True)
        embed.add_field(name="الآيات", value=str(info['verses']), inline=True)
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="tafsir", description="تفسير آية")
    async def tafsir(interaction: discord.Interaction, surah: int, ayah: int):
        if not 1 <= surah <= 114:
            await interaction.response.send_message("❌ رقم السورة 1-114", ephemeral=True)
            return
        result = get_tafsir(surah, ayah)
        if not result.get("success"):
            await interaction.response.send_message("❌ حدث خطأ", ephemeral=True)
            return
        embed = discord.Embed(title=f"📖 تفسير ({surah}:{ayah})", description=result['text'], color=discord.Color.purple())
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="search_semantic", description="بحث دلالي")
    async def search_semantic(interaction: discord.Interaction, query: str):
        try:
            await interaction.response.defer()
            results = semantic_search(query)
            if not results:
                await interaction.followup.send("❌ لا نتائج")
                return
            embed = discord.Embed(title=f"🔍 بحث: {query}", color=discord.Color.blue())
            for i, result in enumerate(results[:3], 1):
                embed.add_field(name=f"#{i}", value=result[:500], inline=False)
            await interaction.followup.send(embed=embed)
        except:
            await interaction.followup.send("❌ حدث خطأ")

    @bot.tree.command(name="quran_page", description="صفحة عشوائية")
    async def quran_page(interaction: discord.Interaction):
        page = random.randint(1, 604)
        embed = discord.Embed(title=f"📖 صفحة {page}", description=f"صفحة {page} من 604", color=discord.Color.teal())
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="quran_juz", description="جزء من القرآن")
    async def quran_juz(interaction: discord.Interaction, juz: int = None):
        if juz is None:
            juz = random.randint(1, 30)
        if not 1 <= juz <= 30:
            await interaction.response.send_message("❌ رقم الجزء 1-30", ephemeral=True)
            return
        embed = discord.Embed(title=f"📚 الجزء {juz} من 30", color=discord.Color.teal())
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="verse_by_topic", description="آية حسب الموضوع")
    async def verse_by_topic(interaction: discord.Interaction, topic: str):
        results = semantic_search(topic)
        if results:
            embed = discord.Embed(title=f"📖 آيات عن: {topic}", description=results[0], color=discord.Color.teal())
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ لا نتائج", ephemeral=True)

    @bot.tree.command(name="memorization_tip", description="نصيحة للحفظ")
    async def memorization_tip(interaction: discord.Interaction):
        tips = ["🎯 اجعل ورداً يومياً", "🔁 راجع ما حفظت", "📖 افهم المعنى", "🎧 استمع للتلاوة", "🤲 ادعُ الله"]
        await interaction.response.send_message(random.choice(tips))

    @bot.tree.command(name="quran_challenge", description="تحدي حفظ")
    async def quran_challenge(interaction: discord.Interaction):
        challenges = ["🎯 احفظ 5 آيات", "🎯 احفظ سورة الكوثر", "🎯 ختم جزء عم", "🎯 راجع 10 صفحات"]
        await interaction.response.send_message(random.choice(challenges))

    # ============================================================
    # HADITH (8 commands)
    # ============================================================

    @bot.tree.command(name="hadith", description="حديث عشوائي")
    async def hadith(interaction: discord.Interaction, collection: str = None):
        try:
            h = get_random_hadith(collection)
            if "error" in h:
                await interaction.response.send_message(f"❌ {h['error']}", ephemeral=True)
                return
            embed = discord.Embed(title=f"📚 {h['collection']}", description=h['text'], color=discord.Color.orange())
            embed.add_field(name="الراوي", value=h.get('narrator', 'غير معروف'), inline=True)
            await interaction.response.send_message(embed=embed)
        except:
            await interaction.response.send_message("❌ حدث خطأ", ephemeral=True)

    @bot.tree.command(name="hadith_collection", description="حديث من مصدر")
    async def hadith_collection(interaction: discord.Interaction, name: str):
        await hadith.callback(interaction, name)

    @bot.tree.command(name="hadith_40_nawawi", description="الأربعين النووية")
    async def hadith_40_nawawi(interaction: discord.Interaction, number: int = None):
        nawawi = [
            {"text": "إِنَّمَا الأَعْمَالُ بِالنِّيَّاتِ...", "explanation": "الأعمال تُقاس بنياتها"},
            {"text": "بُنِيَ الإِسْلاَمُ عَلَى خَمْسٍ...", "explanation": "أركان الإسلام"}
        ]
        h = nawawi[(number - 1) % len(nawawi)] if number and 1 <= number <= 40 else random.choice(nawawi)
        embed = discord.Embed(title="📖 من الأربعين النووية", description=h['text'], color=discord.Color.gold())
        embed.add_field(name="الشرح", value=h['explanation'], inline=False)
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="daily_hadith", description="الحديث اليومي")
    async def daily_hadith(interaction: discord.Interaction):
        await hadith.callback(interaction, None)

    @bot.tree.command(name="hadith_search", description="بحث في الأحاديث")
    async def hadith_search(interaction: discord.Interaction, keyword: str):
        await interaction.response.send_message(f"🔍 بحث عن: {keyword}")

    @bot.tree.command(name="hadith_explain", description="شرح حديث")
    async def hadith_explain(interaction: discord.Interaction, number: int):
        await interaction.response.send_message(f"📖 شرح الحديث {number}")

    @bot.tree.command(name="hadith_quiz", description="اختبار حديث")
    async def hadith_quiz(interaction: discord.Interaction):
        quizzes = [
            {"question": "من قائل: 'إنما الأعمال بالنيات'؟", "hint": "حديث صحيح البخاري"},
            {"question": "كم ركناً للإسلام؟", "hint": "5 أركان"}
        ]
        quiz = random.choice(quizzes)
        await interaction.response.send_message(f"❓ **اختبار**\n\n{quiz['question']}\n💡 {quiz['hint']}")

    @bot.tree.command(name="fortress_muslim", description="حصن المسلم")
    async def fortress_muslim(interaction: discord.Interaction):
        fortress = ["أَصْبَحْنَا وَأَصْبَحَ الْمُلْكُ لِلَّهِ...", "اللَّهُمَّ بِكَ أَصْبَحْنَا..."]
        await interaction.response.send_message(f"🛡️ **حصن المسلم:**\n\n{random.choice(fortress)}")

    # ============================================================
    # AZKAR (8 commands)
    # ============================================================

    @bot.tree.command(name="zikr", description="أذكار صباح/مساء")
    async def zikr(interaction: discord.Interaction, time: str = "morning"):
        try:
            time = time.lower()
            if time not in ["morning", "evening"]:
                await interaction.response.send_message("❌ اختر morning أو evening", ephemeral=True)
                return
            z = get_zikr(time)
            emoji = "🌅" if time == "morning" else "🌙"
            name = "أذكار الصباح" if time == "morning" else "أذكار المساء"
            embed = discord.Embed(title=f"{emoji} {name}", description=z, color=discord.Color.gold())
            await interaction.response.send_message(embed=embed)
        except:
            await interaction.response.send_message("❌ حدث خطأ", ephemeral=True)

    @bot.tree.command(name="tasbeeh", description="تسبيح")
    async def tasbeeh(interaction: discord.Interaction):
        tasbeehat = ["سُبْحَانَ اللَّهِ", "الْحَمْدُ لِلَّهِ", "اللَّهُ أَكْبَرُ"]
        embed = discord.Embed(title="📿 تسبيح", description=random.choice(tasbeehat), color=discord.Color.green())
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="tasbeeh_counter", description="مسبحة إلكترونية")
    async def tasbeeh_counter(interaction: discord.Interaction, dhikr: str = "سبحان الله"):
        await interaction.response.send_message(f"📿 **مسبحة**\n\nالذكر: {dhikr}\nعدد: 0/33")

    @bot.tree.command(name="daily_azkar", description="أذكار يومية")
    async def daily_azkar(interaction: discord.Interaction):
        await interaction.response.send_message("📅 **الأذكار اليومية**\n🌅 صباح - 🌙 مساء - 📿 تسبيح")

    @bot.tree.command(name="dua_situation", description="دعاء للمواقف")
    async def dua_situation(interaction: discord.Interaction, situation: str):
        try:
            result = get_dua(situation)
            embed = discord.Embed(title=f"🤲 دعاء {situation}", description=result['dua'], color=discord.Color.green())
            await interaction.response.send_message(embed=embed)
        except:
            await interaction.response.send_message("❌ الحالات: travel, eating, sleep, studying, sick")

    @bot.tree.command(name="masnoon_dua", description="أدعية مأثورة")
    async def masnoon_dua(interaction: discord.Interaction):
        masnoon = ["رَبِّ اغْفِرْ لِي", "اللَّهُمَّ أَعِنِّي عَلَى ذِكْرِكَ"]
        await interaction.response.send_message(f"📿 **دعاء مأثور:**\n{random.choice(masnoon)}")

    @bot.tree.command(name="ruqyah", description="الرقية الشرعية")
    async def ruqyah(interaction: discord.Interaction):
        await interaction.response.send_message("🛡️ **الرقية الشرعية**\n\nقُلْ أَعُوذُ بِرَبِّ النَّاسِ...")

    @bot.tree.command(name="istikhara", description="دعاء الاستخارة")
    async def istikhara(interaction: discord.Interaction):
        await interaction.response.send_message("🤲 **دعاء الاستخارة**\n\nاللَّهُمَّ إِنِّي أَسْتَخِيرُكَ...")

    # ============================================================
    # PRAYER (8 commands)
    # ============================================================

    @bot.tree.command(name="prayer_times", description="مواقيت الصلاة")
    async def prayer_times(interaction: discord.Interaction, city: str = "Mecca", country: str = "Saudi Arabia"):
        try:
            await interaction.response.defer()
            result = get_prayer_times(city, country)
            if not result.get("success"):
                await interaction.followup.send("❌ حدث خطأ", ephemeral=True)
                return
            times = result['times']
            embed = discord.Embed(title=f"🕌 {result['city']}", description=f"📅 {result['date']}", color=discord.Color.dark_green())
            prayers = [("🌅 الفجر", times['Fajr']), ("🌞 الظهر", times['Dhuhr']), ("☁️ العصر", times['Asr']), ("🌇 المغرب", times['Maghrib']), ("🌙 العشاء", times['Isha'])]
            for name, time in prayers:
                embed.add_field(name=name, value=time, inline=True)
            await interaction.followup.send(embed=embed)
        except:
            await interaction.followup.send("❌ حدث خطأ")

    @bot.tree.command(name="next_prayer", description="الصلاة القادمة")
    async def next_prayer_cmd(interaction: discord.Interaction):
        try:
            result = get_prayer_times()
            next_p = get_next_prayer(result)
            if next_p:
                await interaction.response.send_message(f"🕌 **القادمة:** {next_p}")
            else:
                await interaction.response.send_message("❌ لا يمكن التحديد")
        except:
            await interaction.response.send_message("❌ حدث خطأ", ephemeral=True)

    @bot.tree.command(name="prayer_track", description="تتبع الصلاة")
    async def prayer_track(interaction: discord.Interaction, prayer: str, status: str = "completed"):
        user_id = str(interaction.user.id)
        if track_prayer(user_id, prayer, status):
            await interaction.response.send_message(f"✅ تم تسجيل صلاة {prayer}", ephemeral=True)
        else:
            await interaction.response.send_message("❌ حدث خطأ", ephemeral=True)

    @bot.tree.command(name="qada_track", description="تتبع القضاء")
    async def qada_track(interaction: discord.Interaction, prayer: str, count: int = 1):
        user_id = str(interaction.user.id)
        if track_qada_prayers(user_id, prayer, count):
            await interaction.response.send_message(f"✅ تم إضافة {count} صلاة قضاء لـ {prayer}", ephemeral=True)
        else:
            await interaction.response.send_message("❌ حدث خطأ", ephemeral=True)

    @bot.tree.command(name="prayer_stats", description="إحصائيات الصلاة")
    async def prayer_stats(interaction: discord.Interaction, days: int = 7):
        user_id = str(interaction.user.id)
        stats = get_prayer_stats(user_id, days)
        if stats:
            await interaction.response.send_message(f"📊 **إحصائيات {days} يوم**\n```\n{stats}\n```", ephemeral=True)
        else:
            await interaction.response.send_message("📭 لا توجد إحصائيات", ephemeral=True)

    @bot.tree.command(name="mosque_finder", description="البحث عن مساجد")
    async def mosque_finder(interaction: discord.Interaction, location: str = None):
        await interaction.response.send_message(f"🕌 **البحث عن مساجد**\nالموقع: {location or 'القريبة منك'}\n(ميزة قيد التطوير)")

    @bot.tree.command(name="adhan", description="تفعيل الأذان")
    async def adhan(interaction: discord.Interaction, channel: discord.TextChannel = None):
        await interaction.response.send_message(f"🔔 **الأذان**\nسيتم الإعلان في: {channel.name if channel else 'هذه القناة'}")

    # ============================================================
    # ISLAMIC KNOWLEDGE (8 commands)
    # ============================================================

    @bot.tree.command(name="names_allah", description="أسماء الله الحسنى")
    async def names_allah(interaction: discord.Interaction):
        name = get_random_name_of_allah()
        embed = discord.Embed(title=f"✨ {name['name']}", color=discord.Color.gold())
        embed.add_field(name="اللفظ", value=name['transliteration'], inline=True)
        embed.add_field(name="المعنى", value=name['meaning'], inline=True)
        embed.add_field(name="الشرح", value=name['description'], inline=False)
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="islamic_quiz", description="مسابقة إسلامية")
    async def islamic_quiz(interaction: discord.Interaction):
        quiz = get_islamic_quiz()
        options = "\n".join([f"{i+1}. {opt}" for i, opt in enumerate(quiz['options'])])
        await interaction.response.send_message(f"❓ **سؤال:**\n{quiz['question']}\n\n{options}\n\n💡 استخدم `/quiz_answer` للإجابة")

    @bot.tree.command(name="islamic_fact", description="معلومة إسلامية")
    async def islamic_fact(interaction: discord.Interaction):
        facts = [
            "🌙 القرآن 114 سورة",
            "📖 أول آية نزلت: اقرأ",
            "🕌 البقعة المباركة: مكة",
            "✨ سورة الإخلاص = ثلث القرآن"
        ]
        await interaction.response.send_message(random.choice(facts))

    @bot.tree.command(name="golden_quote", description="حكمة ذهبية")
    async def golden_quote(interaction: discord.Interaction):
        quote = get_islamic_quote()
        await interaction.response.send_message(f"💎 **حكمة:**\n{quote}")

    @bot.tree.command(name="seerah", description="سيرة نبوية")
    async def seerah(interaction: discord.Interaction, topic: str = None):
        seerah_topics = {
            "birth": "ولد النبي ﷺ في عام الفيل",
            "prophethood": "بعثة النبي ﷺ في غار حراء",
            "hijrah": "الهجرة من مكة إلى المدينة",
            "badr": "غزوة بدر الكبرى",
            "conquest": "فتح مكة المكرمة",
            "death": "وفاة النبي ﷺ في المدينة"
        }
        if topic and topic in seerah_topics:
            await interaction.response.send_message(f"📖 **سيرة:**\n{seerah_topics[topic]}")
        else:
            topics_list = ", ".join(seerah_topics.keys())
            await interaction.response.send_message(f"📖 **السيرة النبوية**\nالمواضيع المتاحة: {topics_list}")

    @bot.tree.command(name="fiqh_ruling", description="حكم فقهي")
    async def fiqh_ruling(interaction: discord.Interaction, topic: str = None):
        rulings = {
            "wudu": "الوضوء: فرض غسل الوجه واليدين والمسح على الرأس وغسل الرجلين",
            "prayer": "الصلاة: ركن من أركان الإسلام",
            "fasting": "الصيام: فرض في شهر رمضان"
        }
        if topic and topic in rulings:
            await interaction.response.send_message(f"⚖️ **حكم فقهي:**\n{rulings[topic]}")
        else:
            await interaction.response.send_message(f"⚖️ **الفقه**\nالمواضيع: {', '.join(rulings.keys())}")

    @bot.tree.command(name="islamic_date", description="التاريخ الهجري")
    async def islamic_date(interaction: discord.Interaction):
        from datetime import datetime
        today = datetime.now()
        await interaction.response.send_message(f"📅 **التاريخ**\nميلادي: {today.strftime('%Y-%m-%d')}\nهجري: 1445-{today.month}-{today.day}")

    # ============================================================
    # TRACKING (6 commands)
    # ============================================================

    @bot.tree.command(name="fasting_track", description="تتبع الصيام")
    async def fasting_track(interaction: discord.Interaction, status: str = "fasted"):
        user_id = str(interaction.user.id)
        if track_fasting(user_id, status=status):
            await interaction.response.send_message(f"✅ تم تسجيل: {status}", ephemeral=True)
        else:
            await interaction.response.send_message("❌ حدث خطأ", ephemeral=True)

    @bot.tree.command(name="quran_track", description="تتبع قراءة القرآن")
    async def quran_track(interaction: discord.Interaction, surah: int, verses: int):
        user_id = str(interaction.user.id)
        if track_quran_reading(user_id, surah, verses):
            await interaction.response.send_message(f"✅ تم تسجيل قراءة {verses} آية من سورة {surah}", ephemeral=True)
        else:
            await interaction.response.send_message("❌ حدث خطأ", ephemeral=True)

    @bot.tree.command(name="khatm_progress", description="تقدم الختمة")
    async def khatm_progress(interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        progress = get_khatm_progress(user_id)
        await interaction.response.send_message(f"📊 **تقدم الختمة**\n✅ {progress['completed_surahs']}/114 سورة\n📈 {progress['progress_percentage']}%")

    @bot.tree.command(name="streaks", description="سلسلة الإنجازات")
    async def streaks(interaction: discord.Interaction):
        await interaction.response.send_message("🔥 **سلسلة الإنجازات**\nصلاتك: 7 أيام متتالية\nقراءة القرآن: 3 أيام\nالأذكار: 5 أيام")

    @bot.tree.command(name="islamic_goals", description="الأهداف الإسلامية")
    async def islamic_goals(interaction: discord.Interaction):
        await interaction.response.send_message("🎯 **أهدافك**\n1. ختم القرآن هذا الشهر\n2. صلاة الفجر في المسجد\n3. قراءة 100 صفحة\n4. صيام الاثنين والخميس")

    @bot.tree.command(name="weekly_report", description="التقرير الأسبوعي")
    async def weekly_report(interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        stats = get_quran_reading_stats(user_id, 7)
        await interaction.response.send_message(f"📊 **تقرير الأسبوع**\n📖 آيات: {stats['total_verses']}\n📚 سور: {stats['surahs_read']}\n📅 أيام: {stats['days_read']}")

    # ============================================================
    # FAVORITES (3 commands)
    # ============================================================

    @bot.tree.command(name="favorites", description="عرض المفضلة")
    async def favorites(interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        favs = get_user_favorites(user_id)
        if not favs:
            await interaction.response.send_message("📭 قائمة المفضلة فارغة", ephemeral=True)
            return
        await interaction.response.send_message(f"⭐ **المفضلة**\nعدد العناصر: {len(favs)}")

    @bot.tree.command(name="add_favorite", description="إضافة للمفضلة")
    async def add_favorite_cmd(interaction: discord.Interaction, type: str, id: str):
        user_id = str(interaction.user.id)
        if add_favorite(user_id, type, id):
            await interaction.response.send_message(f"✅ تمت الإضافة", ephemeral=True)
        else:
            await interaction.response.send_message("⚠️ موجود بالفعل", ephemeral=True)

    @bot.tree.command(name="remove_favorite", description="حذف من المفضلة")
    async def remove_favorite_cmd(interaction: discord.Interaction, type: str, id: str):
        user_id = str(interaction.user.id)
        if remove_favorite(user_id, type, id):
            await interaction.response.send_message("✅ تم الحذف", ephemeral=True)
        else:
            await interaction.response.send_message("⚠️ غير موجود", ephemeral=True)

    # ============================================================
    # NEW FEATURES - Islamic Calendar, Qibla, Tasbeeh, Collections
    # ============================================================

    # Islamic Calendar Commands
    @bot.tree.command(name="islamic_calendar", description="التقويم الهجري")
    async def islamic_calendar(interaction: discord.Interaction):
        from services.islamic_calendar_service import get_islamic_date, get_upcoming_holiday
        date_info = get_islamic_date()
        holiday = get_upcoming_holiday()
        
        embed = discord.Embed(title="📅 التقويم الهجري", color=discord.Color.gold())
        embed.add_field(name="التاريخ الهجري", value=date_info['formatted'], inline=True)
        embed.add_field(name="السنة", value=str(date_info['year']), inline=True)
        if holiday:
            embed.add_field(name=f"🎉 {holiday['name']}", value=f"بعد {holiday['days_left']} يوم", inline=False)
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="hijri_month", description="معلومات عن شهر هجري")
    async def hijri_month(interaction: discord.Interaction, month_number: int):
        from services.islamic_calendar_service import get_month_info
        info = get_month_info(month_number)
        if info:
            embed = discord.Embed(title=f"📅 شهر {info['name']}", description=info['significance'], color=discord.Color.gold())
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ رقم الشهر يجب أن يكون بين 1 و 12", ephemeral=True)

    # Qibla Direction Commands
    @bot.tree.command(name="qibla", description="اتجاه القبلة")
    async def qibla_cmd(interaction: discord.Interaction, latitude: float = None, longitude: float = None):
        from services.qibla_service import calculate_qibla_direction, get_qibla_for_major_cities
        
        if latitude and longitude:
            qibla = calculate_qibla_direction(latitude, longitude)
            if "error" not in qibla:
                embed = discord.Embed(title="🕋 اتجاه القبلة", color=discord.Color.green())
                embed.add_field(name="الزاوية", value=f"{qibla['direction_degrees']}°", inline=True)
                embed.add_field(name="الاتجاه", value=qibla['cardinal_direction'], inline=True)
                embed.add_field(name="المسافة", value=f"{qibla['distance_km']} كم", inline=True)
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message("❌ خطأ في الحساب", ephemeral=True)
        else:
            cities = get_qibla_for_major_cities()
            embed = discord.Embed(title="🕋 اتجاه القبلة لمدن رئيسية", color=discord.Color.green())
            for city, data in list(cities.items())[:6]:
                embed.add_field(name=city, value=f"{data['direction']} ({data['degrees']}°)", inline=True)
            await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="qibla_cities", description="اتجاه القبلة للمدن")
    async def qibla_cities(interaction: discord.Interaction):
        from services.qibla_service import get_qibla_for_major_cities
        cities = get_qibla_for_major_cities()
        message = "🕋 **اتجاه القبلة:**\n\n"
        for city, data in cities.items():
            message += f"**{city}**: {data['direction']} ({data['degrees']}°) - {data.get('distance_km', 'N/A')} كم\n"
        await interaction.response.send_message(message[:2000])

    # Enhanced Tasbeeh Counter
    @bot.tree.command(name="tasbeeh_start", description="بدء مسبحة تفاعلية")
    async def tasbeeh_start(interaction: discord.Interaction, dhikr: str = "سبحان الله", target: int = 33):
        embed = discord.Embed(
            title=f"📿 مسبحة {dhikr}",
            description=f"**الهدف:** {target}\n**العدد الحالي:** 0\n\nاضغط على الزر أدناه لكل تسبيحة!",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="tasbeeh_save", description="حفظ تسبيحاتك")
    async def tasbeeh_save(interaction: discord.Interaction, dhikr: str, count: int):
        user_id = str(interaction.user.id)
        if track_tasbeeh(user_id, dhikr, count):
            await interaction.response.send_message(f"✅ تم حفظ {count} من {dhikr}", ephemeral=True)
        else:
            await interaction.response.send_message("❌ حدث خطأ", ephemeral=True)

    # Ramadan Collection
    @bot.tree.command(name="ramadan_countdown", description="عداد رمضان")
    async def ramadan_countdown(interaction: discord.Interaction):
        from services.ramadan_service import get_ramadan_countdown
        countdown = get_ramadan_countdown()
        embed = discord.Embed(title="🌙 العد التنازلي لرمضان", color=discord.Color.purple())
        embed.add_field(name="الأيام المتبقية", value=str(countdown['days_left']), inline=True)
        embed.add_field(name="التاريخ المتوقع", value=countdown['estimated_date'], inline=True)
        embed.add_field(name="السنة الهجرية", value=str(countdown['hijri_year']), inline=True)
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="ramadan_tip", description="نصيحة لرمضان")
    async def ramadan_tip(interaction: discord.Interaction):
        from services.ramadan_service import get_ramadan_tip
        tip = get_ramadan_tip()
        await interaction.response.send_message(tip)

    @bot.tree.command(name="ramadan_guide", description="دليل رمضان")
    async def ramadan_guide(interaction: discord.Interaction, day: int = None):
        from services.ramadan_service import get_daily_fasting_guide
        if day and 1 <= day <= 30:
            guide = get_daily_fasting_guide(day)
            embed = discord.Embed(title=f"📅 {guide['title']}", color=discord.Color.purple())
            tips = "\n".join([f"• {tip}" for tip in guide['tips']])
            embed.description = tips
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("📖 **دليل رمضان**\nاستخدم `/ramadan_guide [رقم اليوم 1-30]`")

    @bot.tree.command(name="iftar_dua", description="أدعية الإفطار")
    async def iftar_dua(interaction: discord.Interaction):
        from services.ramadan_service import get_iftar_duas
        duas = get_iftar_duas()
        embed = discord.Embed(title="🤲 دعاء الإفطار", description=duas['main']['content'], color=discord.Color.gold())
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="suhoor_guide", description="دليل السحور")
    async def suhoor_guide(interaction: discord.Interaction):
        from services.ramadan_service import get_suhoor_benefits
        suhoor = get_suhoor_benefits()
        embed = discord.Embed(title="🌅 فضل السحور", description=suhoor['hadith']['content'], color=discord.Color.blue())
        benefits = "\n".join([f"• {b}" for b in suhoor['benefits']])
        embed.add_field(name="الفوائد", value=benefits, inline=False)
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="taraweeh", description="دليل صلاة التراويح")
    async def taraweeh(interaction: discord.Interaction):
        from services.ramadan_service import TARAWEEH_GUIDE
        embed = discord.Embed(title="🌙 صلاة التراويح", description=TARAWEEH_GUIDE['description'], color=discord.Color.purple())
        embed.add_field(name="الركعات", value=TARAWEEH_GUIDE['rakats'], inline=True)
        embed.add_field(name="الوقت", value=TARAWEEH_GUIDE['timing'], inline=True)
        virtues = "\n".join([f"• {v}" for v in TARAWEEH_GUIDE['virtues'][:2]])
        embed.add_field(name="الفضائل", value=virtues, inline=False)
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="laylatul_qadr", description="ليلة القدر")
    async def laylatul_qadr(interaction: discord.Interaction):
        from services.ramadan_service import LAYLATUL_QADR_INFO
        embed = discord.Embed(title="✨ ليلة القدر", description=LAYLATUL_QADR_INFO['description'], color=discord.Color.gold())
        signs = "\n".join([f"• {s}" for s in LAYLATUL_QADR_INFO['signs'][:3]])
        embed.add_field(name="علاماتها", value=signs, inline=True)
        actions = "\n".join([f"• {a}" for a in LAYLATUL_QADR_INFO['recommended_actions'][:3]])
        embed.add_field(name="الأعمال المستحبة", value=actions, inline=True)
        await interaction.response.send_message(embed=embed)

    # Hajj & Umrah Collection
    @bot.tree.command(name="hajj_guide", description="دليل الحج")
    async def hajj_guide(interaction: discord.Interaction, day: int = None):
        from services.hajj_umrah_service import get_hajj_day_guide
        if day and day in [8, 9, 10, 11, 12, 13]:
            guide = get_hajj_day_guide(day)
            embed = discord.Embed(title=guide['title'], color=discord.Color.green())
            actions = "\n".join([f"• {a}" for a in guide['actions'][:5]])
            embed.description = actions
            if 'dua' in guide:
                embed.add_field(name="الدعاء", value=guide['dua'], inline=False)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("📖 **دليل الحج**\nالأيام: 8 (التروية)، 9 (عرفة)، 10 (النحر)، 11-13 (التشريق)")

    @bot.tree.command(name="umrah_guide", description="دليل العمرة")
    async def umrah_guide(interaction: discord.Interaction, step: str = None):
        from services.hajj_umrah_service import get_umrah_guide, UMRAH_STEPS
        if step and step in UMRAH_STEPS:
            step_info = UMRAH_STEPS[step]
            embed = discord.Embed(title=f"🕋 {step_info['step']}", color=discord.Color.teal())
            actions = "\n".join([f"• {a}" for a in step_info['actions']])
            embed.description = actions
            if 'restrictions' in step_info:
                restrictions = "\n".join([f"⚠️ {r}" for r in step_info['restrictions'][:3]])
                embed.add_field(name="المحظورات", value=restrictions, inline=False)
            await interaction.response.send_message(embed=embed)
        else:
            guide = get_umrah_guide()
            embed = discord.Embed(title="🕋 خطوات العمرة", color=discord.Color.teal())
            steps_list = "\n".join([f"{i+1}. {s['step']}" for i, s in enumerate(guide['steps'])])
            embed.description = steps_list
            embed.add_field(name="المدة المتوقعة", value=guide['estimated_time'], inline=True)
            await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="hajj_types", description="أنواع الحج")
    async def hajj_types(interaction: discord.Interaction):
        from services.hajj_umrah_service import HAJJ_TYPES
        embed = discord.Embed(title="📿 أنواع الحج", color=discord.Color.green())
        for hajj_type, info in HAJJ_TYPES.items():
            steps_count = len(info['steps'])
            embed.add_field(name=info['name'], value=f"{info['description']}\n({steps_count} خطوات)", inline=True)
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="miqats", description="مواقيت الحج")
    async def miqats(interaction: discord.Interaction):
        from services.hajj_umrah_service import MIQAT_LOCATIONS
        embed = discord.Embed(title="📍 مواقيت الإحرام (الميقات)", color=discord.Color.blue())
        for miqat_id, info in MIQAT_LOCATIONS.items():
            embed.add_field(name=info['name'], value=f"{info['location']}\n{info['distance']}", inline=True)
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="hajj_dua", description="أدعية الحج")
    async def hajj_dua(interaction: discord.Interaction, occasion: str = "tawaf"):
        from services.hajj_umrah_service import HAJJ_DUAS
        duas = HAJJ_DUAS.get(occasion, HAJJ_DUAS['tawaf'])
        dua_text = random.choice(duas)
        await interaction.response.send_message(f"🤲 **دعاء:**\n{dua_text}")

    @bot.tree.command(name="hajj_checklist", description="قائمة استعدادات الحج")
    async def hajj_checklist(interaction: discord.Interaction):
        from services.hajj_umrah_service import get_hajj_preparation_checklist
        checklist = get_hajj_preparation_checklist()
        embed = discord.Embed(title="🎒 قائمة استعدادات الحج", color=discord.Color.orange())
        for category, items in checklist.items():
            items_text = "\n".join([f"☐ {item}" for item in items[:3]])
            embed.add_field(name=category, value=items_text, inline=True)
        await interaction.response.send_message(embed=embed)

    # Sunnah Collection
    @bot.tree.command(name="sunnah_prayers", description="النوافل والسنن")
    async def sunnah_prayers(interaction: discord.Interaction, prayer: str = None):
        from services.sunnah_service import get_sunnah_prayer, SUNNAH_PRAYERS
        if prayer and prayer in SUNNAH_PRAYERS:
            info = get_sunnah_prayer(prayer)
            embed = discord.Embed(title=f"📿 {info['name']}", color=discord.Color.gold())
            embed.add_field(name="الركعات", value=info['rakats'], inline=True)
            embed.add_field(name="الوقت", value=info['time'], inline=True)
            embed.add_field(name="الفضل", value=info['virtue'], inline=False)
            await interaction.response.send_message(embed=embed)
        else:
            prayers_list = "، ".join(SUNNAH_PRAYERS.keys())
            await interaction.response.send_message(f"📿 **السنن المتاحة:**\n{prayers_list}")

    @bot.tree.command(name="sunnah_daily", description="السنة اليومية")
    async def sunnah_daily(interaction: discord.Interaction, time: str = "morning"):
        from services.sunnah_service import get_daily_routine
        routine = get_daily_routine(time)
        if routine:
            embed = discord.Embed(title=f"📿 {routine['title']}", color=discord.Color.gold())
            practices = "\n".join([f"• {p}" for p in routine['practices'][:5]])
            embed.description = practices
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ الوقت: morning, evening, friday, sleep")

    @bot.tree.command(name="sunnah_etiquette", description="آداب السنة")
    async def sunnah_etiquette(interaction: discord.Interaction, occasion: str = "eating"):
        from services.sunnah_service import get_etiquette
        etiquette = get_etiquette(occasion)
        if etiquette:
            embed = discord.Embed(title=f"📿 {etiquette['title']}", color=discord.Color.gold())
            practices = "\n".join([f"• {p}" for p in etiquette['practices'][:5]])
            embed.description = practices
            if 'dua' in etiquette:
                embed.add_field(name="الدعاء", value=etiquette['dua'], inline=False)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ المناسبات: eating, drinking, entering_home, leaving_home, mosque")

    @bot.tree.command(name="sunnah_character", description="أخلاق السنة")
    async def sunnah_character(interaction: discord.Interaction):
        from services.sunnah_service import get_character_sunnah
        trait = get_character_sunnah()
        embed = discord.Embed(title=f"📿 {trait['title']}", description=trait['description'], color=discord.Color.gold())
        embed.add_field(name="التطبيق", value=trait['practice'], inline=False)
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="prophet_routine", description="روتين النبي ﷺ")
    async def prophet_routine(interaction: discord.Interaction):
        from services.sunnah_service import get_prophet_routine
        routine = get_prophet_routine()
        embed = discord.Embed(title="📿 روتين يوم النبي ﷺ", color=discord.Color.gold())
        for time, activities in list(routine.items())[:3]:
            activities_text = "\n".join([f"• {a}" for a in activities[:3]])
            embed.add_field(name=time.replace("_", " ").title(), value=activities_text, inline=True)
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="wudu_sunnah", description="سنن الوضوء")
    async def wudu_sunnah(interaction: discord.Interaction):
        from services.sunnah_service import get_wudu_sunnah
        wudu = get_wudu_sunnah()
        embed = discord.Embed(title="📿 سنن الوضوء", color=discord.Color.blue())
        practices = "\n".join([f"• {p}" for p in wudu['practices']])
        embed.description = practices
        embed.add_field(name="الدعاء بعد الوضوء", value=wudu['dua'], inline=False)
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="sunnah_of_day", description="سنة اليوم")
    async def sunnah_of_day(interaction: discord.Interaction):
        from services.sunnah_service import get_sunnah_of_the_day
        sunnah = get_sunnah_of_the_day()
        await interaction.response.send_message(sunnah)

    @bot.tree.command(name="sunnah_track", description="تتبع السنن")
    async def sunnah_track(interaction: discord.Interaction, sunnah_type: str):
        user_id = str(interaction.user.id)
        await interaction.response.send_message(f"✅ تم تسجيل: {sunnah_type}", ephemeral=True)

    # Reciters Commands
    @bot.tree.command(name="reciters", description="قائمة القراء")
    async def reciters(interaction: discord.Interaction):
        from services.reciters_service import get_reciters_list_formatted
        reciters_text = get_reciters_list_formatted()
        await interaction.response.send_message(reciters_text[:2000])

    @bot.tree.command(name="reciter_info", description="معلومات قارئ")
    async def reciter_info(interaction: discord.Interaction, reciter_id: str):
        from services.reciters_service import get_reciter_info
        info = get_reciter_info(reciter_id)
        if info:
            embed = discord.Embed(title=f"🎙️ {info['name']}", color=discord.Color.blue())
            embed.add_field(name="الاسم الإنجليزي", value=info['name_en'], inline=True)
            embed.add_field(name="اللغة", value=info['language'], inline=True)
            embed.add_field(name="الأسلوب", value=info['style'], inline=True)
            embed.add_field(name="الشعبية", value=info['popularity'], inline=True)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ القارئ غير موجود. استخدم `/reciters` لعرض القائمة")

    @bot.tree.command(name="set_reciter", description="تعيين القارئ المفضل")
    async def set_reciter(interaction: discord.Interaction, reciter_id: str):
        from services.reciters_service import get_reciter_info
        info = get_reciter_info(reciter_id)
        if info:
            await interaction.response.send_message(f"✅ تم تعيين القارئ المفضل: {info['name']}", ephemeral=True)
        else:
            await interaction.response.send_message("❌ القارئ غير موجود", ephemeral=True)

    @bot.tree.command(name="random_reciter", description="قارئ عشوائي")
    async def random_reciter(interaction: discord.Interaction):
        from services.reciters_service import get_random_reciter, get_reciter_info
        reciter_id = get_random_reciter()
        info = get_reciter_info(reciter_id)
        await interaction.response.send_message(f"🎙️ **قارئ مقترح:** {info['name']} (`{reciter_id}`)")


    # ============================================================
    # HOURLY RANDOM MESSAGES & COMPLETE QURAN
    # ============================================================

    @bot.tree.command(name="hourly_messages", description="تفعيل/إلغاء الرسائل الساعية")
    async def hourly_messages(interaction: discord.Interaction):
        from services.hourly_messages_service import setup_hourly_messages_command
        await setup_hourly_messages_command(bot, interaction)

    @bot.tree.command(name="mushaf", description="المصحف الشريف كامل")
    async def mushaf(interaction: discord.Interaction, surah: int = None, ayah: int = None):
        from services.complete_quran_service import get_surah_text, get_ayah_text, get_surah_info_complete
        
        try:
            await interaction.response.defer()
            
            if surah and ayah:
                # Get specific ayah
                if not 1 <= surah <= 114:
                    await interaction.followup.send("❌ رقم السورة يجب أن يكون بين 1 و 114", ephemeral=True)
                    return
                
                ayah_data = get_ayah_text(surah, ayah)
                if ayah_data:
                    embed = discord.Embed(
                        title=f"📖 {ayah_data['ref']}",
                        description=ayah_data['text'],
                        color=discord.Color.teal()
                    )
                    embed.set_footer(text=f"سورة {get_surah_info_complete(surah)['name']} - آية {ayah}")
                    await interaction.followup.send(embed=embed)
                else:
                    await interaction.followup.send("❌ لم يتم العثور على الآية", ephemeral=True)
                    
            elif surah:
                # Get surah
                if not 1 <= surah <= 114:
                    await interaction.followup.send("❌ رقم السورة يجب أن يكون بين 1 و 114", ephemeral=True)
                    return
                
                surah_info = get_surah_info_complete(surah)
                if surah_info:
                    # Get first few ayahs
                    surah_data = get_surah_text(surah, 1, min(10, surah_info['verses']))
                    
                    embed = discord.Embed(
                        title=f"📖 سورة {surah_info['name']}",
                        description=f"آياتها: {surah_info['verses']} | مكان النزول: {surah_info['revelation']}",
                        color=discord.Color.teal()
                    )
                    
                    # Add ayahs
                    ayahs_text = ""
                    for ayah in surah_data['ayahs'][:5]:
                        ayahs_text += f"({ayah['number']}) {ayah['text']}\n\n"
                    
                    if len(ayahs_text) > 4000:
                        ayahs_text = ayahs_text[:4000] + "..."
                    
                    embed.add_field(name="بداية السورة", value=ayahs_text or "...", inline=False)
                    
                    if surah_info['verses'] > 10:
                        embed.add_field(
                            name="📌 ملاحظة", 
                            value=f"لعرض السورة كاملة ({surah_info['verses']} آية)، استخدم موقع المصحف الإلكتروني",
                            inline=False
                        )
                    
                    embed.set_footer(text=f"سورة {surah} من 114 | /mushaf {surah} [رقم الآية]")
                    await interaction.followup.send(embed=embed)
                else:
                    await interaction.followup.send("❌ لم يتم العثور على السورة", ephemeral=True)
                    
            else:
                # Show Quran index
                from services.complete_quran_service import get_quran_stats, QURAN_STRUCTURE
                stats = get_quran_stats()
                
                embed = discord.Embed(
                    title="📖 المصحف الشريف",
                    description=f"**إحصائيات القرآن الكريم**\n"
                               f"📚 إجمالي السور: {stats['total_surahs']}\n"
                               f"📖 إجمالي الآيات: {stats['total_ayahs']}\n"
                               f"🕋 مكية: {stats['makki_surahs']} سورة\n"
                               f"🏠 مدنية: {stats['madani_surahs']} سورة",
                    color=discord.Color.teal()
                )
                
                # Show some surahs
                surahs_list = []
                for i in [1, 2, 36, 55, 67, 112]:
                    if i in QURAN_STRUCTURE:
                        s = QURAN_STRUCTURE[i]
                        surahs_list.append(f"`{i}`. {s['name']} ({s['verses']})")
                
                embed.add_field(
                    name="📌 سور مميزة",
                    value="\n".join(surahs_list),
                    inline=False
                )
                
                embed.add_field(
                    name="🎯 كيفية الاستخدام",
                    value="`/mushaf [رقم السورة]` - عرض السورة\n"
                          "`/mushaf 2 255` - عرض آية الكرسي\n"
                          "`/mushaf 1` - عرض سورة الفاتحة",
                    inline=False
                )
                
                await interaction.followup.send(embed=embed)
                
        except Exception as e:
            print(f"Error in mushaf command: {e}")
            await interaction.followup.send("❌ حدث خطأ في عرض المصحف", ephemeral=True)

    @bot.tree.command(name="quran_search", description="البحث في القرآن")
    async def quran_search(interaction: discord.Interaction, query: str):
        from services.complete_quran_service import search_in_quran
        
        try:
            await interaction.response.defer()
            
            results = search_in_quran(query)
            
            if not results:
                await interaction.followup.send("❌ لم يتم العثور على نتائج", ephemeral=True)
                return
            
            embed = discord.Embed(
                title=f"🔍 نتائج البحث عن: {query}",
                description=f"تم العثور على {len(results)} نتيجة",
                color=discord.Color.blue()
            )
            
            for i, result in enumerate(results[:5], 1):
                text = result['text'][:500] + "..." if len(result['text']) > 500 else result['text']
                embed.add_field(
                    name=f"{i}. {result['ref']}",
                    value=text,
                    inline=False
                )
            
            await interaction.followup.send(embed=embed)
            
        except Exception as e:
            print(f"Error in quran_search: {e}")
            await interaction.followup.send("❌ حدث خطأ في البحث", ephemeral=True)

    @bot.tree.command(name="surah_list", description="قائمة سور القرآن")
    async def surah_list(interaction: discord.Interaction, page: int = 1):
        from services.complete_quran_service import QURAN_STRUCTURE
        
        surahs_per_page = 20
        total_surahs = 114
        total_pages = (total_surahs + surahs_per_page - 1) // surahs_per_page
        
        if page < 1 or page > total_pages:
            await interaction.response.send_message(f"❌ رقم الصفحة يجب أن يكون بين 1 و {total_pages}", ephemeral=True)
            return
        
        start_idx = (page - 1) * surahs_per_page + 1
        end_idx = min(start_idx + surahs_per_page - 1, total_surahs)
        
        embed = discord.Embed(
            title=f"📖 سور القرآن الكريم - الصفحة {page}/{total_pages}",
            color=discord.Color.teal()
        )
        
        surahs_text = ""
        for i in range(start_idx, end_idx + 1):
            if i in QURAN_STRUCTURE:
                s = QURAN_STRUCTURE[i]
                surahs_text += f"`{i:3d}`. {s['name']} - {s['verses']} آية ({s['revelation']})\n"
        
        embed.description = surahs_text
        embed.set_footer(text=f"استخدم /surah_list [رقم الصفحة] | /mushaf [رقم السورة]")
        
        await interaction.response.send_message(embed=embed)


    # ============================================================
    # DIAGNOSTIC COMMANDS
    # ============================================================

    @bot.tree.command(name="test_hourly", description="اختبار الرسائل الساعية")
    async def test_hourly(interaction: discord.Interaction):
        """Test the hourly message system"""
        from services.hourly_messages_service import HourlyMessagesService
        import discord as discord_lib
        
        await interaction.response.defer(ephemeral=True)
        
        try:
            # Create a test service
            test_service = HourlyMessagesService(bot)
            
            # Generate a test message
            message_types = ["dua", "dhikr", "hadith", "ayah"]
            import random
            test_type = random.choice(message_types)
            
            embed = await test_service._generate_message(test_type)
            
            if embed:
                # Send to current channel
                await interaction.followup.send(
                    f"✅ **Test Message ({test_type}):**",
                    embed=embed
                )
                
                # Show configuration
                from db.database import get_connection
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("SELECT COUNT(*) as count FROM scheduled_azkar WHERE schedule_type='hourly_messages' AND is_active=1")
                row = cur.fetchone()
                channel_count = row['count'] if row else 0
                conn.close()
                
                await interaction.followup.send(
                    f"📊 **Configuration:**\n"
                    f"Active channels: {channel_count}\n"
                    f"Next hourly message will be sent to these channels automatically.",
                    ephemeral=True
                )
            else:
                await interaction.followup.send("❌ Failed to generate test message", ephemeral=True)
                
        except Exception as e:
            await interaction.followup.send(f"❌ Error: {str(e)}", ephemeral=True)

    @bot.tree.command(name="check_channels", description="التحقق من القنوات المفعلة")
    async def check_channels(interaction: discord.Interaction):
        """Check configured channels for hourly messages"""
        from db.database import get_connection
        
        try:
            conn = get_connection()
            cur = conn.cursor()
            
            # Get hourly messages channels
            cur.execute("SELECT guild_id, channel_id FROM scheduled_azkar WHERE schedule_type='hourly_messages' AND is_active=1")
            hourly_rows = cur.fetchall()
            
            # Get azkar channels
            cur.execute("SELECT guild_id, channel_id, schedule_type FROM scheduled_azkar WHERE schedule_type IN ('morning', 'evening') AND is_active=1")
            azkar_rows = cur.fetchall()
            conn.close()
            
            embed = discord.Embed(title="📊 قنوات الإشعارات المفعلة", color=discord.Color.blue())
            
            # Hourly messages
            if hourly_rows:
                channels_text = ""
                for row in hourly_rows:
                    channel = bot.get_channel(int(row['channel_id']))
                    channel_name = channel.name if channel else "Unknown"
                    channels_text += f"• {channel_name} (ID: {row['channel_id']})\n"
                embed.add_field(name="⏰ الرسائل الساعية", value=channels_text or "No channels", inline=False)
            else:
                embed.add_field(name="⏰ الرسائل الساعية", value="⚠️ لم يتم تفعيل أي قناة\nاستخدم: `/hourly_messages`", inline=False)
            
            # Azkar channels
            if azkar_rows:
                morning = [r for r in azkar_rows if r['schedule_type'] == 'morning']
                evening = [r for r in azkar_rows if r['schedule_type'] == 'evening']
                embed.add_field(name="🌅 أذكار الصباح", value=f"{len(morning)} قناة", inline=True)
                embed.add_field(name="🌙 أذكار المساء", value=f"{len(evening)} قناة", inline=True)
            else:
                embed.add_field(name="🤲 الأذكار", value="⚠️ لم يتم التفعيل", inline=False)
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {str(e)}", ephemeral=True)

