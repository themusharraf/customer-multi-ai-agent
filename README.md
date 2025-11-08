# CrewAI Qo'llab-quvvatlash Tizimi Arxitekturasi

## 1. Umumiy Tizim Arxitekturasi

```mermaid
graph TB
    subgraph "Tashqi Muhit"
        ENV[Environment Variables]
        OPENAI[OpenAI API]
        DOCS[CrewAI Documentation]
    end

    subgraph "Konfiguratsiya Qatlami"
        CONFIG[Configuration Layer]
        ENV --> CONFIG
        CONFIG --> |API Key| OPENAI_KEY[OPENAI_API_KEY]
        CONFIG --> |Model| MODEL[gpt-4o-mini]
    end

    subgraph "Vositalar Qatlami"
        TOOLS[Tools Layer]
        SCRAPER[docs_scrape_tool]
        TOOLS --> SCRAPER
    end

    subgraph "Agent Qatlami"
        AGENT1[Support Agent<br/>Katta qo'llab-quvvatlash vakili]
        AGENT2[QA Agent<br/>Sifat nazorati mutaxassisi]
        
        SCRAPER -.->|ishlatadi| AGENT1
    end

    subgraph "Vazifa Qatlami"
        TASK1[Inquiry Resolution Task<br/>So'rovni hal qilish]
        TASK2[Quality Assurance Task<br/>Sifat nazorati]
        
        AGENT1 --> TASK1
        AGENT2 --> TASK2
        TASK1 -->|chiqish| TASK2
    end

    subgraph "Orkestratsiya Qatlami"
        CREW[Crew<br/>Memory enabled]
        MEMORY[(Short-term &<br/>Long-term Memory)]
        
        TASK1 --> CREW
        TASK2 --> CREW
        CREW <--> MEMORY
    end

    subgraph "Kirish/Chiqish"
        INPUT[Input Data<br/>customer, person, inquiry]
        OUTPUT[Final Output<br/>Sifatli javob]
        
        INPUT --> CREW
        CREW --> OUTPUT
    end

    OPENAI -.->|API so'rovlar| AGENT1
    OPENAI -.->|API so'rovlar| AGENT2
    DOCS -.->|ma'lumot olish| SCRAPER

```

---

## 2. Ma'lumotlar Oqimi (Data Flow)

```mermaid
sequenceDiagram
    participant User
    participant Crew
    participant Memory
    participant SupportAgent
    participant DocsTools
    participant QAAgent
    participant OpenAI

    User->>Crew: Input (customer, person, inquiry)
    activate Crew
    
    Crew->>Memory: Xotira holatini yuklash
    Memory-->>Crew: Oldingi kontekst
    
    Crew->>SupportAgent: Inquiry Resolution Task
    activate SupportAgent
    
    SupportAgent->>DocsTools: Hujjatlardan qidirish
    activate DocsTools
    DocsTools->>OpenAI: Embedding yaratish
    OpenAI-->>DocsTools: Embeddings
    DocsTools-->>SupportAgent: Tegishli hujjatlar
    deactivate DocsTools
    
    SupportAgent->>OpenAI: Javob generatsiya qilish
    OpenAI-->>SupportAgent: Dastlabki javob
    SupportAgent-->>Crew: Tayyor javob
    deactivate SupportAgent
    
    Crew->>Memory: Natijani saqlash
    
    Crew->>QAAgent: Quality Assurance Task
    activate QAAgent
    
    QAAgent->>OpenAI: Javobni tahlil qilish
    OpenAI-->>QAAgent: Tahlil natijalari
    
    QAAgent->>OpenAI: Yaxshilangan javob
    OpenAI-->>QAAgent: Yakuniy javob
    QAAgent-->>Crew: Tasdiqlangan javob
    deactivate QAAgent
    
    Crew->>Memory: Yakuniy natijani saqlash
    Crew-->>User: Final Output
    deactivate Crew
```

---

## 3. Agent Arxitekturasi

```mermaid
graph LR
    subgraph "Support Agent"
        SA_ROLE[Role: Katta qo'llab-quvvatlash vakili]
        SA_GOAL[Goal: Eng do'stona yordam]
        SA_BACKSTORY[Backstory: CrewAI xodimi]
        SA_TOOLS[Tools: docs_scrape_tool]
        SA_CONFIG[Config: allow_delegation=False]
        
        SA_ROLE --> SA_GOAL
        SA_GOAL --> SA_BACKSTORY
        SA_BACKSTORY --> SA_TOOLS
        SA_TOOLS --> SA_CONFIG
    end

    subgraph "QA Agent"
        QA_ROLE[Role: Sifat nazorati mutaxassisi]
        QA_GOAL[Goal: Eng yaxshi sifatni ta'minlash]
        QA_BACKSTORY[Backstory: Sifat tekshiruvchi]
        QA_CONFIG[Config: default settings]
        
        QA_ROLE --> QA_GOAL
        QA_GOAL --> QA_BACKSTORY
        QA_BACKSTORY --> QA_CONFIG
    end

    SA_CONFIG -.->|Chiqish| QA_ROLE
```

---

## 4. Task Workflow

```mermaid
stateDiagram-v2
    [*] --> InputReceived: User so'rovi
    
    InputReceived --> InquiryResolution: Support Agent boshlanadi
    
    state InquiryResolution {
        [*] --> AnalyzeInquiry
        AnalyzeInquiry --> SearchDocs: docs_scrape_tool
        SearchDocs --> GenerateResponse: OpenAI
        GenerateResponse --> [*]
    }
    
    InquiryResolution --> QualityCheck: Dastlabki javob tayyor
    
    state QualityCheck {
        [*] --> ReviewResponse
        ReviewResponse --> CheckCompleteness
        CheckCompleteness --> CheckAccuracy
        CheckAccuracy --> CheckTone
        CheckTone --> ImproveResponse
        ImproveResponse --> [*]
    }
    
    QualityCheck --> SaveToMemory: Tasdiqlangan javob
    SaveToMemory --> [*]: Final Output

    note right of InquiryResolution
        Tools: docs_scrape_tool
        Agent: Support Agent
        Output: Dastlabki batafsil javob
    end note

    note right of QualityCheck
        Agent: QA Agent
        Output: Yakuniy sifatli javob
    end note
```

---

## 5. Memory Tizimi

```mermaid
graph TB
    subgraph "Memory System"
        STM[Short-term Memory<br/>Joriy suhbat]
        LTM[Long-term Memory<br/>O'tmishdagi suhbatlar]
        ENTITY[Entity Memory<br/>Mijozlar haqida]
        
        CREW_MEM[Crew Memory=True]
        
        CREW_MEM --> STM
        CREW_MEM --> LTM
        CREW_MEM --> ENTITY
    end

    subgraph "Memory Usage"
        CONTEXT[Kontekstni saqlash]
        LEARNING[O'rganish]
        PERSONALIZATION[Shaxsiylashtirish]
        
        STM --> CONTEXT
        LTM --> LEARNING
        ENTITY --> PERSONALIZATION
    end

    subgraph "Benefits"
        CONSISTENCY[Izchillik]
        EFFICIENCY[Samaradorlik]
        QUALITY[Sifat yaxshilanishi]
        
        CONTEXT --> CONSISTENCY
        LEARNING --> EFFICIENCY
        PERSONALIZATION --> QUALITY
    end
```

---

## 6. Komponentlar Bog'lanishi

```mermaid
mindmap
    root((CrewAI System))
        Configuration
            OpenAI API Key
            Model: gpt-4o-mini
            Environment Setup
        Agents
            Support Agent
                Role & Goal
                Backstory
                Tools Access
                No Delegation
            QA Agent
                Role & Goal
                Review Process
                Quality Standards
        Tasks
            Inquiry Resolution
                Description
                Expected Output
                Tool Integration
            Quality Assurance
                Review Criteria
                Final Output
                Tone Check
        Tools
            docs_scrape_tool
                Documentation Access
                Information Retrieval
        Memory
            Short-term
            Long-term
            Entity Memory
        Workflow
            Sequential Processing
            Agent Collaboration
            Memory Integration
```

---

## 7. Best Practices va Takomillashtirish

```mermaid
graph TB
    subgraph "Joriy Arxitektura"
        CURRENT[Hozirgi holat]
        AGENTS[2 ta Agent]
        TASKS[2 ta Task]
        MEMORY[Memory enabled]
        TOOLS[1 ta Tool]
    end

    subgraph "Best Practices"
        BP1[ Sequential workflow]
        BP2[ Memory enabled]
        BP3[ Quality assurance]
        BP4[ Tool integration]
        BP5[ Clear roles]
    end

    subgraph "Takomillashtirish Imkoniyatlari"
        IMP1[+ Qo'shimcha vositalar]
        IMP2[+ Error handling]
        IMP3[+ Logging system]
        IMP4[+ Validation layer]
        IMP5[+ Caching mechanism]
        IMP6[+ Performance monitoring]
    end

    subgraph "Kelajak Arxitekturasi"
        FUTURE[Takomillashtirilgan tizim]
        MORE_AGENTS[Maxsus agentlar]
        MORE_TOOLS[Ko'proq vositalar]
        BETTER_MEMORY[Kengaytirilgan xotira]
        MONITORING[Monitoring & Analytics]
    end

    CURRENT --> BP1
    CURRENT --> BP2
    CURRENT --> BP3
    CURRENT --> BP4
    CURRENT --> BP5

    BP1 --> IMP1
    BP2 --> IMP2
    BP3 --> IMP3
    BP4 --> IMP4
    BP5 --> IMP5

    IMP1 --> FUTURE
    IMP2 --> FUTURE
    IMP3 --> FUTURE
    IMP4 --> FUTURE
    IMP5 --> FUTURE
    IMP6 --> FUTURE

    FUTURE --> MORE_AGENTS
    FUTURE --> MORE_TOOLS
    FUTURE --> BETTER_MEMORY
    FUTURE --> MONITORING

   
```

---

## Asosiy Xususiyatlar

### 1. **Qatlamli Arxitektura**
- Configuration Layer: Muhit sozlamalari
- Tools Layer: Yordamchi vositalar
- Agent Layer: Aqlli agentlar
- Task Layer: Vazifalar
- Orchestration Layer: Crew boshqaruvi

### 2. **Agent Specialization**
- **Support Agent**: Mijoz so'rovlarini hal qilish
- **QA Agent**: Sifatni ta'minlash

### 3. **Memory Integration**
- Short-term memory: Joriy kontekst
- Long-term memory: Tarixiy ma'lumotlar
- Entity memory: Mijozlar haqida bilim

### 4. **Quality Assurance**
- Ikki bosqichli tekshiruv
- Sifat standartlari
- Professional ohang

### 5. **Tool Integration**
- docs_scrape_tool: Hujjatlardan qidirish
- Kengaytiriladigan arxitektura
