import os
from crewai import Agent, Task, Crew, Process, LLM

# ---------------- BEDAVA MODEL AYARLARI ----------------
my_local_llm = LLM(
    model="ollama/llama3.1",
    base_url="http://localhost:11434"
)

# ---------------- KADRO (AJANLAR) ----------------

analyst = Agent(
    role='Expert Business Analyst',
    goal='Web tabanlı oyun gereksinimlerini belirlemek',
    backstory='Web projelerinde uzman bir analistsin.',
    verbose=True,
    llm=my_local_llm
)

developer = Agent(
    role='Senior Python Web Developer',
    goal='Tek dosya halinde çalışan Flask uygulaması yazmak',
    backstory='Flask ve HTML/JS konularında uzmansın. Karmaşık dosya yapıları yerine her şeyi (HTML, CSS, JS) tek bir Python dosyası içine gömerek yazarsın.',
    verbose=True,
    llm=my_local_llm
)

tester = Agent(
    role='QA Engineer',
    goal='Web uygulamasını test etmek',
    backstory='Web sitelerindeki hataları bulursun.',
    verbose=True,
    llm=my_local_llm
)

devops = Agent(
    role='DevOps Engineer',
    goal='Dockerfile hazırlamak',
    backstory='Web uygulamasını buluta taşımak için gerekenleri bilirsin.',
    verbose=True,
    llm=my_local_llm
)

# ---------------- GÖREVLER ----------------

# Senin yeni isteğin burada:
kullanici_istegi = "Bana Python Flask kullanarak tarayıcıda çalışan bir Yılan Oyunu (Snake Game) yap. Oyun HTML Canvas ve JavaScript ile çalışsın ama sunucusu Python Flask olsun."

task1 = Task(
    description=f"İstek: {kullanici_istegi}. Web oyunu için teknik plan yap.",
    agent=analyst,
    expected_output="Teknik plan."
)

task2 = Task(
    description="Analistin planına göre kodu yaz. ÖNEMLİ: HTML dosyasını ayrı verme. 'render_template_string' fonksiyonunu kullanarak HTML ve JavaScript kodlarını Python dosyasının içine göm. Tek bir 'app.py' dosyası istiyorum.",
    agent=developer,
    expected_output="Tam çalışan Python Flask kodu.",
    context=[task1],
    output_file="app.py"  # <--- Dosya adı artık app.py
)

task3 = Task(
    description="app.py kodunu incele. HTML/JS mantığını kontrol et.",
    agent=tester,
    expected_output="Test raporu.",
    context=[task2]
)

task4 = Task(
    description="Bu web uygulaması için Dockerfile hazırla.",
    agent=devops,
    expected_output="Dockerfile içeriği.",
    context=[task2]
)

# ---------------- ÇALIŞTIRMA ----------------

my_company = Crew(
    agents=[analyst, developer, tester, devops],
    tasks=[task1, task2, task3, task4],
    verbose=True,
    process=Process.sequential
)

print("########## WEB EKİBİ ÇALIŞIYOR ##########")
result = my_company.kickoff()

print("\n\n################ İŞLEM TAMAM ################\n")
print("Klasörünü kontrol et, 'app.py' dosyası oluşmuş olmalı!")