import warnings

warnings.filterwarnings('ignore')

from crewai import Agent, Task, Crew
import os
from utils import get_openai_api_key
from tools import docs_scrape_tool

# OpenAI API kalitini olish
openai_api_key = get_openai_api_key()

# Muhit o'zgaruvchisini o'rnatish
os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["OPENAI_MODEL_NAME"] = "gpt-4o-mini"

# Hozircha test uchun chiqish
# print("CrewAI muhit sozlandi! Model:", os.environ["OPENAI_MODEL_NAME"])

support_agent = Agent(
    role="Katta qo‘llab-quvvatlash vakili",
    goal="Jamoangizdagi eng do‘stona va foydali qo‘llab-quvvatlovchi bo‘ling",
    backstory=(
        "Siz crewAI (https://crewai.com) kompaniyasida ishlaysiz va "
        "hozirda {customer} nomli juda muhim mijozga "
        "qo‘llab-quvvatlash xizmati ko‘rsatmoqdasiz. "
        "Sizning vazifangiz — eng yaxshi yordamni taqdim etishdir! "
        "Har bir javobni to‘liq va aniq yozing, "
        "Har bir javobni **O‘ZBEK TILIDA** yozing, "
        "hech qanday taxminlarga yo‘l qo‘ymang."
    ),
    allow_delegation=False,
    verbose=True
)

support_quality_assurance_agent = Agent(
    role="Qo‘llab-quvvatlash sifat nazorati mutaxassisi",
    goal="Jamoangizdagi eng yaxshi qo‘llab-quvvatlash sifatini ta’minlab, e’tirofga sazovor bo‘ling",
    backstory=(
        "Siz crewAI (https://crewai.com) kompaniyasida ishlaysiz va "
        "hozirda jamoangiz bilan birgalikda "
        "{customer} nomli mijozning so‘rovi ustida ishlayapsiz. "
        "Sizning vazifangiz — qo‘llab-quvvatlash vakili "
        "eng yuqori sifatli yordam ko‘rsatayotganini ta’minlashdir. "
        "Qo‘llab-quvvatlash vakili to‘liq va aniq javoblar berayotganini "
        "hamda hech qanday taxminlar qilmayotganini tekshirib boring."
    ),
    verbose=True
)

inquiry_resolution = Task(
    description=(
        "{customer} kompaniyasidan muhim so‘rov yuborildi:\n"
        "{inquiry}\n\n"
        "{customer} kompaniyasidan {person} ushbu murojaatni yuborgan. "
        "Mavjud barcha bilim va vositalardan foydalanib, "
        "mijozga eng yaxshi yordamni ko‘rsatishga harakat qil. "
        "Mijoz so‘roviga to‘liq va aniq javob berishga intilishing kerak."
    ),
    expected_output=(
        "Mijoz so‘roviga batafsil va foydali javob. "
        "Javobda mijoz bergan savolning barcha jihatlari yoritilishi kerak.\n"
        "Javobda foydalanilgan barcha manbalar, "
        "tashqi ma’lumotlar yoki yechimlarga havolalar keltirilsin. "
        "Javob to‘liq bo‘lishi, "
        "hech bir savol javobsiz qolmasligi "
        "va samimiy, yordam beruvchi ohangda yozilishi kerak."
        "samimiy, yordam beruvchi ohangda O‘ZBEK TILIDA yozilishi kerak."
    ),
    tools=[docs_scrape_tool],
    agent=support_agent,
)

quality_assurance_review = Task(
    description=(
        "Katta mijozlarga xizmat ko‘rsatish vakili tayyorlagan javobni ko‘rib chiqing. "
        "Javob mijozga to‘liq, aniq va yuqori sifat standartlariga mos ekanligiga ishonch hosil qiling.\n"
        "Mijoz so‘rovidagi barcha jihatlar yoritilganligini, "
        "javob foydali va samimiy ohangda yozilganini tekshiring.\n"
        "Javobda foydalanilgan manbalar va ma’lumotlarga havolalar mavjudligiga, "
        "javob to‘liq asoslangan va hech bir savol javobsiz qolmaganligiga ishonch hosil qiling."
    ),
    expected_output=(
        "Mijozga yuborishga tayyor, batafsil va foydali yakuniy javob.\n"
        "U mijoz so‘rovining barcha jihatlarini qamrab olgan, "
        "kerakli tuzatishlar va takliflar kiritilgan bo‘lishi kerak.\n"
        "Ohang professional va samimiy bo‘lsin, "
        "ammo juda rasmiy emas — biz erkin va do‘stona kompaniyamiz."
    ),
    agent=support_quality_assurance_agent,
)

crew = Crew(
    agents=[support_agent, support_quality_assurance_agent],
    tasks=[inquiry_resolution, quality_assurance_review],
    verbose=True,
    memory=True,
)

inputs = {
    "customer": "DeepLearningAI",
    "person": "Andrew Ng",
    "inquiry": "Men Crew yaratish va ishga tushirish bo‘yicha yordamga muhtojman. Xususan, crew’ga memory qanday qo‘shish mumkin? Iltimos, ko‘rsatma bera olasizmi?"
}

result = crew.kickoff(inputs=inputs)
