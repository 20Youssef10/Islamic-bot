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
    # HELP & INFO COMMANDS (4)
    # ============================================================

    @bot.tree.command(name="help", description="عرض قائمة الأوامر المتاحة")
    async def help_command(interaction: discord.Interaction):
        """Display help message with all available commands"""
        try:
            embed = discord.Embed(
                title="📖 Islamic Bot - قائمة الأوامر",
                description="**مرحباً بك في البوت الإسلامي الشامل!**\nهذا البوت يحتوي على 50+ أمر إسلامي",
                color=discord.Color.green()
            )
            
            embed.add_field(
                name="📚 القرآن الكريم (10)",
                value="`/ayah`, `/ayah_audio`, `/surah_info`, `/tafsir`, `/search_semantic`, `/quran_page`, `/quran_juz`, `/verse_by_topic`, `/memorization_tip`, `/quran_challenge`",
                inline=False
            )
            
            embed.add_field(
                name="📖 الحديث الشريف (8)",
                value="`/hadith`, `/hadith_collection`, `/hadith_40_nawawi`, `/daily_hadith`, `/hadith_search`, `/hadith_explain`, `/hadith_quiz`, `/fortress_muslim`",
                inline=False
            )
            
            embed.add_field(
                name="🤲 الأذكار والأدعية (8)",
                value="`/zikr`, `/tasbeeh`, `/tasbeeh_counter`, `/daily_azkar`, `/dua_situation`, `/masnoon_dua`, `/ruqyah`, `/istikhara`",
                inline=False
            )
            
            embed.add_field(
                name="🕌 الصلاة (8)",
                value="`/prayer_times`, `/next_prayer`, `/qibla`, `/prayer_track`, `/qada_track`, `/prayer_stats`, `/mosque_finder`, `/adhan`",
                inline=False
            )
            
            embed.add_field(
                name="🎓 المعرفة الإسلامية (8)",
                value="`/names_allah`, `/islamic_quiz`, `/islamic_fact`, `/golden_quote`, `/seerah`, `/fiqh_ruling`, `/islamic_date`, `/ramadan_countdown`",
                inline=False
            )
            
            embed.add_field(
                name="📊 التتبع الشخصي (6)",
                value="`/fasting_track`, `/quran_track`, `/khatm_progress`, `/streaks`, `/islamic_goals`, `/weekly_report`",
                inline=False
            )
            
            embed.set_footer(text="جزاك الله خيراً لاستخدامك البوت الإسلامي 🤲")
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message("❌ حدث خطأ", ephemeral=True)

    @bot.tree.command(name="bot_info", description="معلومات عن البوت")
    async def bot_info(interaction: discord.Interaction):
        embed = discord.Embed(title="🤖 معلومات البوت الإسلامي", color=discord.Color.blue())
        embed.add_field(name="الإصدار", value="2.0", inline=True)
        embed.add_field(name="عدد الأوامر", value="50+", inline=True)
        embed.add_field(name="السور", value="114", inline=True)
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="invite", description="دعوة البوت لسيرفرك")
    async def invite_bot(interaction: discord.Interaction):
        await interaction.response.send_message(
            "🔗 **لدعوة البوت:**\nhttps://discord.com/oauth2/authorize?client_id=1459564811183591686&scope=bot&permissions=2147483647\n\nجزاك الله خيراً!",
            ephemeral=True
        )

    @bot.tree.command(name="settings", description="إعدادات البوت")
    async def settings_cmd(interaction: discord.Interaction):
        await interaction.response.send_message("⚙️ **الإعدادات**\nاستخدم `/set_city` و `/set_country` لتحديد موقعك", ephemeral=True)

    # ============================================================
    # QURAN COMMANDS (10)
    # ============================================================

    @bot.tree.command(name="ayah", description="آية قرآنية عشوائية")
    async def ayah(interaction: discord.Interaction):
        try:
            a = get_random_ayah()
            embed = discord.Embed(title=a['ref'], description=a['text'], color=discord.Color.teal())
            embed.set_footer(text=f"آية رقم: {a['id']}")
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message("❌ عذراً، حدث خطأ", ephemeral=True)

    @bot.tree.command(name="ayah_audio", description="آية مع تلاوة صوتية")
    async def ayah_audio(interaction: discord.Interaction, reciter: str = "ar.alafasy"):
        try:
            await interaction.response.defer()
            a = get_random_ayah()
            audio = get_audio(a["id"], reciter)
            embed = discord.Embed(title=f"🎧 {a['ref']}", description=a['text'], color=discord.Color.teal())
            await interaction.followup.send(embed=embed, file=discord.File(audio))
        except Exception as e:
            await interaction.followup.send("❌ عذراً، حدث خطأ")

    @bot.tree.command(name="surah_info", description="معلومات عن سورة")
    async def surah_info(interaction: discord.Interaction, surah_number: int):
        if surah_number < 1 or surah_number > 114:
            await interaction.response.send_message("❌ رقم السورة يجب أن يكون بين 1 و 114", ephemeral=True)
            return
        info = get_surah_info(surah_number)
        embed = discord.Embed(title=f"📖 سورة {info['name']}", color=discord.Color.teal())
        embed.add_field(name="المعنى", value=info['meaning'], inline=True)
        embed.add_field(name="الآيات", value=str(info['verses']), inline=True)
        embed.add_field(name="النزول", value=info['revelation'], inline=True)
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="tafsir", description="تفسير آية من القرآن")
    async def tafsir(interaction: discord.Interaction, surah: int, ayah: int, source: str = "ibn-kathir"):
        if surah < 1 or surah > 114:
            await interaction.response.send_message("❌ رقم السورة يجب أن يكون بين 1 و 114", ephemeral=True)
            return
        result = get_tafsir(surah, ayah, source)
        if not result.get("success"):
            await interaction.response.send_message(f"❌ {result.get('error', 'حدث خطأ')}", ephemeral=True)
            return
        info = get_surah_info(surah)
        embed = discord.Embed(title=f"📖 تفسير سورة {info['name']} ({surah}:{ayah})", description=result['text'], color=discord.Color.purple())
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="search_semantic", description="بحث دلالي في القرآن")
    async def search_semantic(interaction: discord.Interaction, query: str):
        try:
            await interaction.response.defer()
            results = semantic_search(query)
            if not results:
                await interaction.followup.send("❌ لم يتم العثور على نتائج")
                return
            embed = discord.Embed(title=f"🔍 نتائج البحث: {query}", color=discord.Color.blue())
            for i, result in enumerate(results[:3], 1):
                embed.add_field(name=f"#{i}", value=result[:500], inline=False)
            await interaction.followup.send(embed=embed)
        except Exception as e:
            await interaction.followup.send("❌ عذراً، حدث خطأ")

    @bot.tree.command(name="quran_page", description="صفحة عشوائية من المصحف")
    async def quran_page(interaction: discord.Interaction):
        page = random.randint(1, 604)
        embed = discord.Embed(title=f"📖 صفحة المصحف #{page}", description=f"اقرأ صفحة من القرآن\nالصفحة {page} من 604", color=discord.Color.teal())
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="quran_juz", description="جزء من القرآن")
    async def quran_juz(interaction: discord.Interaction, juz: int = None):
        if juz is None:
            juz = random.randint(1, 30)
        if juz < 1 or juz > 30:
            await interaction.response.send_message("❌ رقم الجزء يجب أن يكون بين 1 و 30", ephemeral=True)
            return
        embed = discord.Embed(title=f"📚 الجزء {juz} من 30", color=discord.Color.teal())
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="verse_by_topic", description="آية حسب الموضوع")
    async def verse_by_topic(interaction: discord.Interaction, topic: str):
        topics_map = {"رحمة": "mercy", "صبر": "patience", "دعاء": "prayer", "جنة": "paradise", "نار": "hell"}
        search_term = topics_map.get(topic, topic)
        results = semantic_search(search_term)
        if results:
            embed = discord.Embed(title=f"📖 آيات عن: {topic}", description=results[0], color=discord.Color.teal())
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ لم يتم العثور على آيات", ephemeral=True)

    @bot.tree.command(name="memorization_tip", description="نصيحة لحفظ القرآن")
    async def memorization_tip(interaction: discord.Interaction):
        tips = [
            "🎯 **اجعل لك ورداً يومياً** - الاستمرار أهم من الكمية",
            "🔁 **راجع ما حفظت** - التكرار يثبت الحفظ",
            "📖 **افهم المعنى** - يساعد على التثبيت",
            "🎧 **استمع للتلاوة** - يحسن التلاوة",
            "🤲 **ادعُ الله** - سلم الله أن يجعل القرآن ربيع قلبك"
        ]
        await interaction.response.send_message(random.choice(tips))

    @bot.tree.command(name="quran_challenge", description="تحدي حفظ القرآن")
    async def quran_challenge(interaction: discord.Interaction):
        challenges = [
            "🎯 **تحدي اليوم**: احفظ 5 آيات من سورة يس",
            "🎯 **تحدي الأسبوع**: احفظ سورة الكوثر كاملة",
            "🎯 **تحدي الشهر**: ختم جزء عم كاملاً",
            "🎯 **التحدي الذهبي**: راجع 10 صفحات من الحفظ"
        ]
        await interaction.response.send_message(random.choice(challenges))
