# ============================================================
# add_tech_categories.py - IMPROVED VERSION
# Adds 50+ tech categories with detailed resume text
# RUN: python add_tech_categories.py
# ============================================================

import pandas as pd
import os

print("Loading existing dataset...")
df_existing = pd.read_csv('UpdatedResumeDataSet.csv')

# Normalize column names
if 'Resume_str' in df_existing.columns:
    df_existing = df_existing.rename(columns={'Resume_str': 'Resume'})

df_existing = df_existing[['Category', 'Resume']].dropna()
print(f"Existing: {len(df_existing)} resumes, {df_existing['Category'].nunique()} categories")

tech_resumes = []

def add(category, resumes):
    for r in resumes:
        tech_resumes.append({'Category': category, 'Resume': r})

# Each category gets 3 different detailed resume variations

add('DATA-SCIENCE', [
    """Experienced Data Scientist with 5 years specializing in machine learning predictive modeling statistical analysis. 
    Proficient Python R TensorFlow PyTorch scikit-learn pandas numpy matplotlib seaborn. 
    Built recommendation systems fraud detection natural language processing pipelines computer vision models. 
    Experience deep learning neural networks convolutional recurrent transformer architectures. 
    SQL PostgreSQL MongoDB data wrangling feature engineering model deployment AWS SageMaker. 
    Strong statistics probability linear algebra calculus optimization algorithms. 
    Published research papers machine learning conferences NeurIPS ICML. 
    Experience A/B testing hypothesis testing statistical inference data storytelling.""",

    """Data Scientist specializing artificial intelligence machine learning deep learning applications. 
    Python expert pandas scikit-learn XGBoost LightGBM CatBoost ensemble methods. 
    Natural language processing BERT GPT transformers text classification sentiment analysis. 
    Computer vision image recognition object detection YOLO ResNet CNN architectures. 
    Big data Spark Hadoop distributed computing cloud AWS GCP Azure platforms. 
    Data visualization Tableau Power BI matplotlib plotly dashboard development. 
    Strong mathematical background regression classification clustering dimensionality reduction. 
    Deployed production machine learning models Docker Kubernetes FastAPI REST APIs.""",

    """Senior Data Scientist leading analytics team delivering business intelligence insights. 
    Expert Python R SQL machine learning statistical modeling predictive analytics. 
    TensorFlow Keras PyTorch neural network training hyperparameter optimization. 
    Time series forecasting anomaly detection customer segmentation churn prediction. 
    Data pipeline Apache Airflow ETL processing feature stores MLflow experiment tracking. 
    Cross functional collaboration product engineering business stakeholders communication. 
    Mentored junior data scientists established best practices machine learning workflow. 
    Published three patents machine learning optimization algorithms."""
])

add('DATA-ANALYST', [
    """Data Analyst with expertise translating complex data into actionable business insights. 
    Proficient SQL advanced queries joins subqueries window functions stored procedures. 
    Excel pivot tables VLOOKUP advanced formulas data cleaning manipulation. 
    Tableau Power BI Looker dashboard development KPI reporting visualization. 
    Python pandas numpy data analysis statistical testing hypothesis testing. 
    Google Analytics Adobe Analytics web analytics digital marketing metrics. 
    Experience retail finance healthcare domains data driven decision making. 
    Strong communication presenting findings executives non technical stakeholders.""",

    """Business Data Analyst specializing financial analysis reporting performance metrics. 
    SQL Server MySQL PostgreSQL database querying data extraction transformation. 
    Power BI Tableau QlikView interactive dashboards executive reporting automation. 
    Python R statistical analysis regression analysis forecasting modeling. 
    Data quality validation cleansing governance documentation standards. 
    A/B testing experimentation analysis conversion optimization user behavior. 
    Collaborated cross functional teams marketing sales operations product management. 
    Reduced reporting time 60 percent automated manual processes Python scripts.""",

    """Junior Data Analyst passionate uncovering insights data visualization storytelling. 
    Strong SQL skills complex queries aggregations data manipulation transformation. 
    Excel advanced functions pivot tables charts conditional formatting dashboards. 
    Tableau Power BI creating interactive reports stakeholder presentations. 
    Python basics pandas data cleaning exploratory data analysis visualization. 
    Statistical knowledge descriptive statistics correlation regression analysis. 
    Detail oriented analytical thinking problem solving communication skills. 
    Internship experience e-commerce startup analyzing user behavior conversion funnels."""
])

add('MACHINE-LEARNING-ENGINEER', [
    """Machine Learning Engineer building deploying scalable ML systems production environment. 
    Expert Python TensorFlow PyTorch Keras scikit-learn XGBoost model development. 
    MLOps model serving monitoring retraining pipelines automated deployment. 
    Feature engineering feature stores Feast Tecton data preprocessing pipelines. 
    Docker Kubernetes Kubeflow MLflow model registry experiment tracking versioning. 
    AWS SageMaker Azure ML Google Vertex AI cloud machine learning platforms. 
    Distributed training GPU optimization CUDA TensorRT model quantization pruning. 
    Designed recommendation engine serving 10 million users daily low latency inference.""",

    """ML Engineer specializing natural language processing large language model deployment. 
    Hugging Face transformers BERT GPT T5 fine tuning custom downstream tasks. 
    Python PyTorch JAX distributed training multi GPU multi node clusters. 
    Model compression knowledge distillation ONNX export edge deployment mobile. 
    Real time inference optimization batch prediction asynchronous processing queues. 
    Kafka streaming data pipelines real time feature computation model serving. 
    Strong software engineering skills clean code testing CI/CD best practices. 
    Reduced model inference latency 40 percent optimization techniques production.""",

    """Machine Learning Engineer computer vision autonomous systems perception pipeline. 
    OpenCV YOLO Detectron2 image classification segmentation object detection tracking. 
    Python C++ real time video processing camera calibration depth estimation. 
    CUDA GPU programming parallel computing neural network optimization deployment. 
    Embedded systems Jetson Nano Raspberry Pi edge AI model optimization TensorRT. 
    Data annotation labeling pipelines augmentation techniques training data quality. 
    Built pedestrian detection system autonomous vehicle 99 percent accuracy production. 
    Experience medical imaging pathology slide analysis diagnostic AI systems."""
])

add('SOFTWARE-ENGINEER', [
    """Software Engineer 6 years experience building scalable distributed systems. 
    Expert Python Java Go microservices REST APIs system design architecture. 
    React Node.js TypeScript frontend backend full stack development. 
    PostgreSQL MySQL MongoDB Redis database design optimization indexing. 
    Docker Kubernetes cloud AWS GCP deployment infrastructure automation. 
    Agile Scrum sprint planning code review technical documentation mentoring. 
    Designed payment processing system handling 50000 transactions per second. 
    Strong data structures algorithms competitive programming problem solving skills.""",

    """Backend Software Engineer specializing high performance distributed systems. 
    Java Spring Boot Hibernate microservices event driven architecture Kafka. 
    Python Django FastAPI REST GraphQL API design development deployment. 
    PostgreSQL MySQL Redis Elasticsearch database management optimization. 
    Kubernetes Docker Helm Terraform infrastructure code cloud AWS Azure. 
    System design scalability reliability fault tolerance distributed consensus. 
    Implemented caching strategy reducing database load 70 percent improved latency. 
    Open source contributor popular frameworks libraries GitHub community active.""",

    """Full Stack Software Engineer building web applications products users love. 
    React TypeScript Redux frontend state management component architecture. 
    Node.js Express Python Flask backend API development authentication. 
    PostgreSQL MongoDB database schema design ORM Prisma Sequelize. 
    AWS EC2 S3 Lambda serverless deployment CI/CD GitHub Actions pipelines. 
    Agile methodology sprint ceremonies stakeholder communication product mindset. 
    Led migration monolith microservices architecture improved deployment frequency. 
    Strong testing practices unit integration end to end TDD BDD methodologies."""
])

add('FRONTEND-DEVELOPER', [
    """Frontend Developer expert React TypeScript building modern web applications. 
    React hooks context Redux Zustand state management component design patterns. 
    TypeScript strict mode generics utility types advanced type system mastery. 
    Next.js server side rendering static generation API routes performance optimization. 
    CSS Tailwind Styled Components animations transitions responsive mobile first design. 
    GraphQL Apollo Client REST API integration WebSocket real time features. 
    Webpack Vite bundle optimization code splitting lazy loading performance metrics. 
    Accessibility WCAG 2.1 standards screen readers keyboard navigation inclusive design.""",

    """Senior Frontend Developer leading UI architecture large scale React applications. 
    React performance optimization memo useMemo useCallback virtual DOM reconciliation. 
    Design system component library Storybook documentation token based theming. 
    TypeScript advanced patterns generics decorators mapped conditional types. 
    Testing Jest React Testing Library Cypress end to end integration coverage. 
    Web performance Core Web Vitals Lighthouse optimization image loading strategies. 
    Mentored five junior developers established coding standards review processes. 
    Built dashboard application 200 complex components used 500 enterprise customers.""",

    """Frontend Developer specializing interactive data visualization dashboard development. 
    React D3.js Recharts Chart.js complex data visualization interactive graphics. 
    TypeScript JavaScript ES6 modern features async await promises functional programming. 
    Responsive design CSS Grid Flexbox mobile tablet desktop cross browser compatibility. 
    REST API integration authentication JWT OAuth2 secure frontend practices. 
    Performance optimization lazy loading infinite scroll virtual lists large datasets. 
    Collaborated closely designers Figma pixel perfect implementation animations. 
    Built real time analytics dashboard processing 100000 data points smooth rendering."""
])

add('BACKEND-DEVELOPER', [
    """Backend Developer specializing high performance API development microservices. 
    Python FastAPI Django REST Framework async programming concurrent request handling. 
    PostgreSQL advanced queries indexing partitioning replication performance tuning. 
    Redis caching session management pub sub message queuing rate limiting. 
    Docker Kubernetes service mesh Istio load balancing health checks deployment. 
    Message queues RabbitMQ Kafka event driven asynchronous processing workflows. 
    Security OAuth2 JWT API authentication authorization RBAC implementation. 
    Designed API gateway handling 100000 requests per minute 99.9 percent uptime.""",

    """Java Backend Developer enterprise application development Spring ecosystem expert. 
    Spring Boot Spring MVC Spring Security Spring Data JPA Hibernate ORM. 
    Microservices architecture service discovery Eureka load balancing Ribbon Feign. 
    PostgreSQL Oracle MySQL database design stored procedures triggers optimization. 
    Apache Kafka event streaming CQRS event sourcing domain driven design patterns. 
    Docker Kubernetes Jenkins CI/CD automated testing deployment production. 
    Design patterns Factory Builder Observer Strategy clean code SOLID principles. 
    Led backend migration improving system throughput 300 percent reduced response time.""",

    """Node.js Backend Developer building scalable real time applications APIs. 
    Node.js Express NestJS TypeScript backend REST GraphQL API development. 
    MongoDB PostgreSQL Redis database management ODM ORM Mongoose Prisma. 
    Socket.io WebSocket real time communication chat notification systems. 
    AWS Lambda API Gateway S3 serverless architecture cost optimization. 
    Authentication Passport.js JWT OAuth2 social login security best practices. 
    Testing Mocha Chai Jest supertest API integration unit testing coverage. 
    Built real time collaboration platform supporting 10000 concurrent users."""
])

add('DEVOPS-ENGINEER', [
    """DevOps Engineer automating infrastructure deployment accelerating development velocity. 
    Kubernetes Helm ArgoCD GitOps deployment strategies blue green canary releases. 
    Terraform Ansible infrastructure code provisioning configuration management. 
    CI/CD Jenkins GitHub Actions GitLab CI automated testing deployment pipelines. 
    Docker containerization multi stage builds optimization security scanning. 
    AWS EC2 EKS RDS S3 CloudFormation cloud architecture cost optimization. 
    Prometheus Grafana alerting monitoring observability distributed tracing Jaeger. 
    Reduced deployment time 80 percent zero downtime deployment strategy implementation.""",

    """Senior DevOps Engineer building developer platforms internal tooling infrastructure. 
    Platform engineering developer experience tooling automation productivity improvement. 
    Kubernetes operator development custom controllers admission webhooks CRDs. 
    HashiCorp Vault secrets management Terraform cloud infrastructure GitOps workflows. 
    Security scanning Trivy Snyk SAST DAST DevSecOps pipeline integration. 
    AWS Azure multi cloud strategy networking VPC peering transit gateway configuration. 
    SLO SLA error budget incident management postmortem blameless culture champion. 
    Built internal developer platform reducing new service onboarding 3 days 2 hours.""",

    """Cloud DevOps Engineer specializing AWS infrastructure reliability engineering. 
    AWS Solutions Architect certified EC2 ECS EKS Lambda RDS Aurora CloudFront. 
    Terraform modules reusable infrastructure components multi environment management. 
    Docker Kubernetes deployment scaling auto scaling horizontal vertical pod autoscaler. 
    Datadog monitoring APM logging distributed tracing alert management on call. 
    Python bash scripting automation operational tasks runbooks documentation. 
    Disaster recovery backup strategies RTO RPO business continuity planning. 
    Managed infrastructure supporting 5 million daily active users 99.99 percent uptime."""
])

add('CYBERSECURITY-ENGINEER', [
    """Cybersecurity Engineer protecting enterprise systems applications data threats. 
    Penetration testing vulnerability assessment OWASP Top 10 web application security. 
    SIEM Splunk ELK stack threat detection incident response digital forensics. 
    Python bash scripting security automation threat hunting custom tooling. 
    Network security firewall IDS IPS VPN zero trust architecture implementation. 
    Cloud security AWS Security Hub Azure Sentinel GCP Security Command Center. 
    CISSP CEH OSCP certifications compliance GDPR HIPAA SOC2 PCI DSS frameworks. 
    Identified critical vulnerability financial application preventing 10M data breach.""",

    """Application Security Engineer integrating security software development lifecycle. 
    SAST DAST SCA security testing tools integration CI/CD pipeline automation. 
    Code review security vulnerability identification remediation guidance developers. 
    Threat modeling STRIDE PASTA risk assessment security architecture review. 
    Bug bounty program experience HackerOne Bugcrowd responsible disclosure. 
    Web application security XSS CSRF SQL injection authentication bypass testing. 
    Security champions program developer security training awareness education. 
    Reduced critical vulnerabilities 90 percent through automated scanning processes.""",

    """Cloud Security Engineer securing multi cloud infrastructure applications data. 
    AWS Azure GCP security services IAM policies least privilege access control. 
    Container security Kubernetes RBAC network policies pod security standards. 
    Secrets management HashiCorp Vault AWS Secrets Manager encryption key rotation. 
    Compliance automation infrastructure security checks policy as code OPA Rego. 
    Security incident response playbooks forensic investigation threat containment. 
    Zero trust network access ZTNA identity verification microsegmentation implementation. 
    Implemented security program achieving SOC2 Type II certification six months."""
])

add('MOBILE-DEVELOPER', [
    """Mobile Developer iOS Android cross platform application development expert. 
    React Native Flutter Dart cross platform mobile development shared codebase. 
    iOS Swift SwiftUI UIKit Xcode App Store deployment TestFlight beta testing. 
    Android Kotlin Java Jetpack Compose Android Studio Play Store publishing. 
    REST API Firebase Supabase backend integration push notifications in app purchases. 
    Mobile UI UX best practices gesture navigation animations performance optimization. 
    Offline functionality SQLite local storage sync conflict resolution strategies. 
    Published 8 mobile applications combined 2 million downloads positive ratings.""",

    """iOS Developer native iPhone iPad application Swift SwiftUI expert. 
    Swift advanced concurrency async await actors Combine reactive programming. 
    SwiftUI complex custom views animations transitions state management. 
    Core Data CloudKit local remote data persistence synchronization. 
    Networking URLSession Alamofire Moya REST GraphQL API integration. 
    ARKit RealityKit augmented reality spatial computing Vision framework. 
    Core ML on device machine learning model inference privacy preserving AI. 
    Shipping five apps App Store 4.8 average rating featured Apple editorial.""",

    """Android Developer Kotlin Jetpack modern Android development expert. 
    Kotlin coroutines Flow StateFlow SharedFlow reactive asynchronous programming. 
    Jetpack Compose modern declarative UI development Material Design 3. 
    Architecture components ViewModel LiveData Room Navigation Hilt dependency injection. 
    Work Manager background processing constraints chaining parallel tasks. 
    Firebase Authentication Firestore Analytics Crashlytics Remote Config integration. 
    Modularization multi module project structure build time optimization. 
    Accessibility TalkBack content descriptions touch target size requirements."""
])

add('AI-ENGINEER', [
    """AI Engineer building production artificial intelligence systems large scale deployment. 
    Large language models GPT Claude Llama fine tuning prompt engineering RAG systems. 
    LangChain LlamaIndex vector databases Pinecone Weaviate semantic search retrieval. 
    Python PyTorch Hugging Face transformers model training evaluation deployment. 
    MLOps model serving monitoring drift detection retraining automation pipelines. 
    Multimodal AI vision language models image text understanding generation systems. 
    AI safety alignment evaluation red teaming bias detection fairness testing. 
    Built enterprise chatbot LLM reducing customer support tickets 60 percent.""",

    """Generative AI Engineer specializing foundation models applications enterprise. 
    OpenAI API Anthropic Claude Google Gemini LLM integration application development. 
    Retrieval augmented generation RAG vector embeddings semantic chunking strategies. 
    Fine tuning LoRA QLoRA PEFT parameter efficient training custom domains. 
    Prompt engineering chain of thought few shot instruction following optimization. 
    Agent frameworks AutoGPT LangGraph tool use function calling autonomous systems. 
    Evaluation frameworks benchmarking hallucination detection factuality assessment. 
    Deployed AI assistant processing 100000 queries daily enterprise knowledge base.""",

    """AI Research Engineer bridging research production state art model deployment. 
    Deep learning computer vision natural language processing multimodal systems. 
    PyTorch JAX custom CUDA kernels GPU optimization distributed training strategies. 
    Diffusion models stable diffusion fine tuning image generation creative AI. 
    Reinforcement learning RLHF reward modeling preference optimization alignment. 
    Benchmark evaluation academic datasets GLUE SuperGLUE ImageNet COCO metrics. 
    Research engineering reproduce papers novel architectures ablation studies. 
    Published NeurIPS workshop paper novel efficient attention mechanism transformer."""
])

add('CLOUD-ENGINEER', [
    """Cloud Engineer AWS certified designing scalable reliable cloud infrastructure. 
    AWS EC2 ECS EKS Lambda RDS Aurora DynamoDB S3 CloudFront Route53 expertise. 
    Infrastructure code Terraform CloudFormation modules reusable components. 
    Cost optimization reserved instances spot instances rightsizing savings plans. 
    High availability multi AZ disaster recovery backup restoration procedures. 
    Networking VPC subnets security groups NACLs VPN Direct Connect Transit Gateway. 
    Monitoring CloudWatch X-Ray distributed tracing alerting operational dashboards. 
    Migrated legacy on premise applications AWS saving 40 percent infrastructure costs.""",

    """Multi Cloud Engineer Azure GCP AWS designing hybrid cloud solutions enterprise. 
    Azure AKS Azure Functions Cosmos DB Azure DevOps Microsoft cloud ecosystem. 
    Google Cloud GKE Cloud Run BigQuery Pub Sub Dataflow analytics workloads. 
    Kubernetes multi cloud federation service mesh Istio cross cluster traffic. 
    FinOps cloud cost management budgets alerts tagging governance policies. 
    Security compliance cloud controls CSPM posture management remediation automation. 
    Cloud native architecture microservices serverless event driven design patterns. 
    Architected multi cloud strategy achieving 99.99 percent availability global regions.""",

    """Cloud Infrastructure Engineer specializing Kubernetes platform engineering. 
    Kubernetes cluster administration upgrades node management storage networking. 
    Helm chart development packaging deployment templating values management. 
    Service mesh Istio traffic management mTLS observability policy enforcement. 
    Container registry Harbor image scanning vulnerability management policies. 
    GitOps ArgoCD Flux automated deployment reconciliation drift detection. 
    Storage solutions Ceph Longhorn persistent volumes stateful application management. 
    Built Kubernetes platform 50 development teams 300 microservices production."""
])

add('DATA-ENGINEER', [
    """Data Engineer building scalable data infrastructure pipelines analytics platforms. 
    Apache Spark distributed data processing PySpark SQL batch streaming workloads. 
    Apache Kafka real time event streaming data pipeline ingestion processing. 
    Airflow orchestration DAG development scheduling dependency management monitoring. 
    dbt data transformation modeling testing documentation data warehouse. 
    Snowflake BigQuery Redshift cloud data warehouse optimization performance tuning. 
    Python Scala SQL data processing ETL ELT pipeline development testing. 
    Built data platform processing 10TB daily enabling self serve analytics 200 users.""",

    """Senior Data Engineer designing implementing enterprise data lakehouse architecture. 
    Delta Lake Apache Iceberg table format ACID transactions schema evolution. 
    Databricks unified analytics platform MLflow experiment model deployment. 
    Spark streaming Kafka Flink real time analytics low latency processing. 
    Data quality Great Expectations validation testing monitoring alerting. 
    Metadata catalog Apache Atlas data lineage governance documentation. 
    Python advanced pandas polars dask distributed dataframe processing. 
    Led migration traditional data warehouse modern lakehouse architecture savings.""",

    """Data Engineer specializing cloud native data platform AWS GCP Azure. 
    AWS Glue EMR Athena Lake Formation data lake architecture governance. 
    GCP Dataflow Dataproc BigQuery Pub Sub streaming batch processing. 
    Terraform infrastructure code reproducible data platform deployment. 
    Kafka Connect CDC change data capture database streaming Debezium. 
    Star schema dimensional modeling slowly changing dimensions data vault. 
    Apache Hudi incremental processing upserts deletes GDPR compliance deletion. 
    Reduced data pipeline costs 50 percent optimization cloud resource usage."""
])

add('BLOCKCHAIN-DEVELOPER', [
    """Blockchain Developer Ethereum Solidity smart contract development DeFi protocols. 
    Solidity advanced patterns upgradeable proxy contracts gas optimization security. 
    Hardhat Foundry Truffle smart contract testing deployment verification tools. 
    DeFi protocols AMM liquidity pools yield farming staking governance mechanics. 
    NFT ERC721 ERC1155 marketplace royalty standards metadata IPFS storage. 
    Web3.js Ethers.js frontend blockchain integration wallet connection MetaMask. 
    Security audit Slither Mythril manual review common vulnerability patterns. 
    Deployed DeFi protocol 50 million TVL zero security incidents production.""",

    """Web3 Developer building decentralized applications full stack blockchain. 
    Solidity Rust smart contract development Ethereum Solana ecosystems. 
    React TypeScript Next.js frontend dApp development wallet integration. 
    IPFS Filecoin decentralized storage NFT metadata immutable content addressing. 
    Layer 2 Polygon Arbitrum Optimism zkSync scaling solutions deployment. 
    Chainlink oracle integration price feeds VRF randomness automation keepers. 
    DAO governance Snapshot Tally voting delegation proposal execution contracts. 
    Built NFT marketplace 10000 ETH trading volume first month launch.""",

    """Blockchain Infrastructure Engineer node operation protocol development. 
    Ethereum node Geth Erigon operation maintenance sync monitoring performance. 
    Validator staking Ethereum 2.0 consensus client Prysm Lighthouse operation. 
    Go Rust low level blockchain client development protocol implementation. 
    MEV maximal extractable value research flash bots bundle submission strategies. 
    Cross chain bridge development asset transfer message passing security. 
    Smart contract indexing The Graph subgraph development query optimization. 
    Operated validator infrastructure 99.9 percent uptime slashing incident free."""
])

add('GAME-DEVELOPER', [
    """Game Developer Unity engine C# mobile PC console game development. 
    Unity advanced features DOTS ECS job system burst compiler performance. 
    C# design patterns observer command state machine gameplay programming. 
    Physics simulation rigidbody collision detection pathfinding NavMesh AI. 
    Shader HLSL custom rendering pipeline post processing visual effects. 
    Multiplayer Photon Mirror Unity Netcode networking synchronization. 
    Mobile optimization texture compression LOD batching profiling memory. 
    Published strategy game 500000 downloads 4.7 Play Store App Store rating.""",

    """Unreal Engine Developer C++ AAA game development technical art shader. 
    Unreal C++ Blueprint hybrid development gameplay mechanics systems. 
    Niagara particle systems visual effects destruction physics simulation. 
    Lumen Nanite next generation rendering global illumination virtualized geometry. 
    Multiplayer dedicated server replication lag compensation prediction. 
    Animation Blueprint blend trees state machines procedural IK systems. 
    Performance profiling GPU CPU optimization frame budget management. 
    Shipped AAA title 2 million copies sold metacritic 87 score positive reviews.""",

    """Indie Game Developer Unity Godot solo developer published multiple games. 
    Game design document scope management feature prioritization ship mentality. 
    2D 3D art pipeline integration animation rigging sprite sheet optimization. 
    Procedural generation level algorithms noise functions roguelike systems. 
    Steam Itch.io publishing marketing community management player feedback. 
    Monetization in app purchases ads subscription premium indie business model. 
    GDScript C# scripting gameplay UI systems save load progression management. 
    Three games published Steam positive reviews 85 percent average community."""
])

add('FULL-STACK-DEVELOPER', [
    """Full Stack Developer React Node.js Python building end to end web applications. 
    React TypeScript hooks context modern frontend development component architecture. 
    Node.js Express Python Django REST API backend development authentication. 
    PostgreSQL MongoDB Redis database design integration ORM Sequelize Prisma. 
    AWS deployment Docker containerization CI/CD GitHub Actions automation. 
    GraphQL Apollo Server Client schema design resolver implementation. 
    Testing Jest Pytest React Testing Library end to end Playwright Cypress. 
    Built SaaS platform 0 to 10000 users leading technical decisions architecture.""",

    """MERN Stack Developer MongoDB Express React Node.js specialist. 
    React advanced patterns custom hooks context performance optimization. 
    Node.js Express REST API development middleware authentication JWT. 
    MongoDB Mongoose schema design aggregation pipeline indexing optimization. 
    Redux Toolkit state management async thunk RTK Query data fetching caching. 
    Socket.io real time features WebSocket chat notifications live updates. 
    AWS EC2 S3 deployment NGINX reverse proxy SSL configuration production. 
    Freelance full stack developer delivered 20 client projects positive feedback.""",

    """Full Stack Engineer Python React technical lead small startup team. 
    Python FastAPI async backend high performance REST API microservices. 
    React TypeScript Next.js full stack framework SSR SSG ISR deployment. 
    PostgreSQL Alembic migrations database design normalization optimization. 
    Celery Redis background task processing scheduled jobs async workflows. 
    Docker Compose local development Kubernetes production deployment scaling. 
    Technical interviews hiring process code review standards documentation. 
    Grew startup product 0 revenue 1M ARR leading 3 person engineering team."""
])

# Add more categories with similar detailed approach
add('QA-ENGINEER', [
    """QA Engineer automation manual testing ensuring software quality reliability. 
    Selenium WebDriver Python Java automated browser testing cross browser. 
    Cypress modern JavaScript testing framework component integration end to end. 
    API testing Postman REST Assured Newman automated collection execution CI. 
    Performance testing JMeter Gatling load stress spike testing production readiness. 
    Mobile testing Appium iOS Android real device cloud BrowserStack Sauce Labs. 
    Agile testing practices sprint ceremonies bug reporting Jira defect lifecycle. 
    Built automation framework reducing regression testing 80 percent manual effort.""",

    """Senior QA Engineer test strategy quality processes team leadership. 
    Test planning strategy risk based testing exploratory charter based approaches. 
    Selenium TestNG data driven keyword driven hybrid automation frameworks. 
    BDD Cucumber Gherkin acceptance criteria automation behavior specification. 
    CI/CD pipeline integration Jenkins GitHub Actions test gate quality checks. 
    Performance security accessibility testing comprehensive quality coverage. 
    Metrics reporting defect density test coverage quality dashboards management. 
    Established QA practice zero defect escape production three consecutive quarters.""",

    """QA Automation Engineer Python pytest building robust test infrastructure. 
    Python pytest fixtures parametrize markers advanced testing patterns. 
    Playwright async Python browser automation modern web application testing. 
    API contract testing Pact consumer driven contracts microservices validation. 
    Visual regression Percy Applitools pixel comparison screenshot testing. 
    Database testing data validation SQL assertions ETL pipeline quality checks. 
    Docker test containers isolated environment reproducible testing infrastructure. 
    Reduced production bugs 75 percent comprehensive automated testing coverage."""
])

add('NETWORK-ENGINEER', [
    """Network Engineer designing managing enterprise network infrastructure operations. 
    Cisco Juniper routing switching OSPF BGP EIGRP MPLS WAN optimization. 
    Firewall Palo Alto Fortinet Cisco ASA security policy management VPN. 
    SD-WAN software defined networking Viptela Meraki CloudGenix deployment. 
    Network monitoring SolarWinds PRTG Nagios performance baseline troubleshooting. 
    Data center networking spine leaf Cisco ACI VMware NSX microsegmentation. 
    Python network automation Netmiko NAPALM Ansible network configuration management. 
    Designed campus network 10000 users zero downtime migration legacy infrastructure.""",

    """Cloud Network Engineer AWS Azure hybrid connectivity architecture design. 
    AWS VPC subnet design security groups NACLs Transit Gateway Direct Connect. 
    Azure Virtual Network ExpressRoute VPN Gateway peering hub spoke topology. 
    Network security zero trust microsegmentation east west traffic inspection. 
    DNS CDN load balancer global traffic management Route53 CloudFlare Akamai. 
    IPv6 migration dual stack deployment planning addressing scheme documentation. 
    Network automation Terraform provider infrastructure code repeatable deployment. 
    Implemented zero trust network reducing attack surface lateral movement prevention.""",

    """Network Security Engineer protecting infrastructure perimeter internal segmentation. 
    Next generation firewall deep packet inspection application layer filtering. 
    Intrusion detection prevention system signature tuning false positive reduction. 
    Network access control NAC 802.1X RADIUS authentication wired wireless. 
    VPN IPSec SSL TLS remote access site to site corporate connectivity. 
    DDoS mitigation traffic scrubbing BGP blackholing anycast protection measures. 
    Packet analysis Wireshark tcpdump network forensics incident investigation. 
    Responded 50 security incidents zero data breach network perimeter protection."""
])

add('DATABASE-ADMINISTRATOR', [
    """Database Administrator PostgreSQL MySQL Oracle managing enterprise databases. 
    PostgreSQL advanced features partitioning replication streaming logical WAL. 
    Performance tuning query optimization execution plan analysis index strategy. 
    High availability Patroni PgBouncer connection pooling failover automation. 
    Backup recovery PITR point in time recovery disaster testing documentation. 
    Database security access control row level security encryption at rest transit. 
    Migration data modeling schema design normalization third normal form. 
    Managed 50TB PostgreSQL cluster 99.999 percent uptime financial application.""",

    """NoSQL Database Administrator MongoDB Cassandra Redis Elasticsearch specialist. 
    MongoDB replica set sharding aggregation pipeline performance optimization. 
    Cassandra data modeling partition key clustering column compaction strategies. 
    Redis cluster sentinel pub sub Lua scripting cache eviction policies. 
    Elasticsearch mapping index lifecycle management snapshot restore operations. 
    DynamoDB single table design access patterns capacity planning auto scaling. 
    Multi model database strategy polyglot persistence selection right tool. 
    Designed database architecture supporting 1 billion documents MongoDB production.""",

    """Cloud Database Engineer AWS RDS Aurora Snowflake managed service expertise. 
    RDS Aurora PostgreSQL MySQL parameter groups enhanced monitoring performance. 
    DynamoDB advanced patterns GSI LSI transactions streams DynamoDB Accelerator. 
    Snowflake virtual warehouses data sharing time travel zero copy cloning. 
    Database migration AWS DMS Schema Conversion Tool heterogeneous migration. 
    Cost optimization storage tiering archiving lifecycle policies compression. 
    Terraform infrastructure code reproducible database provisioning configuration. 
    Migrated 10 on premise databases AWS RDS 30 percent performance improvement."""
])

add('PRODUCT-MANAGER-TECH', [
    """Technical Product Manager 5 years driving product strategy roadmap execution. 
    Product roadmap prioritization RICE framework stakeholder alignment OKR setting. 
    User research interviews usability testing persona development journey mapping. 
    Data driven decisions SQL analytics Amplitude Mixpanel funnel analysis metrics. 
    Agile Scrum ceremonies sprint planning refinement review retrospective facilitation. 
    Technical background API design system architecture tradeoff discussions engineers. 
    Go to market strategy launch planning pricing positioning competitive analysis. 
    Launched 3 products 0 to 1 million users leading cross functional teams delivery.""",

    """Senior Product Manager platform developer tools internal product experience. 
    Developer experience DX metrics DORA metrics deployment frequency lead time. 
    API product strategy versioning deprecation developer documentation adoption. 
    Technical roadmap prioritization engineering debt balance feature development. 
    Stakeholder management C suite communication quarterly business review presentation. 
    Pricing strategy monetization freemium premium enterprise tier packaging. 
    Product analytics North Star metric weekly active users engagement retention. 
    Grew developer platform 500 to 50000 monthly active developers two years.""",

    """Associate Product Manager technical background software engineering transition. 
    Requirements gathering user stories acceptance criteria edge case documentation. 
    Jira Confluence Linear project management documentation knowledge base. 
    A/B testing hypothesis driven experimentation statistical significance analysis. 
    Competitive analysis market research TAM SAM SOM opportunity sizing. 
    Wireframing Figma low fidelity prototype user feedback iteration validation. 
    Cross functional collaboration design engineering marketing sales alignment. 
    First PM hire startup built product process 0 framework established team culture."""
])

add('UI-UX-DESIGNER', [
    """UI/UX Designer creating intuitive user centered digital experiences products. 
    Figma expert component library design system auto layout variant prototyping. 
    User research moderated unmoderated usability testing insight synthesis. 
    Information architecture site map user flow task analysis mental model mapping. 
    Visual design typography color theory spacing grid system composition principles. 
    Interaction design microinteraction animation transition state change feedback. 
    Accessibility WCAG 2.1 AA color contrast keyboard navigation screen reader. 
    Redesigned checkout flow increasing conversion rate 35 percent A/B tested validated.""",

    """Senior UX Designer leading design systems cross product consistency experience. 
    Design system component library token documentation Storybook integration. 
    Strategic UX research longitudinal diary study contextual inquiry field research. 
    Service design blueprint stakeholder journey end to end experience orchestration. 
    Facilitation design sprint workshop ideation diverge converge prototype test. 
    Figma advanced prototyping variables conditional logic complex interaction design. 
    Data informed design analytics heatmap session recording behavior analysis. 
    Built design system adopted 8 product teams 100 components tokens documented.""",

    """Product Designer end to end ownership discovery definition design delivery. 
    Discovery problem framing hypothesis generation assumption mapping validation. 
    Figma high fidelity pixel perfect spec handoff developer collaboration Zeplin. 
    Mobile first iOS Android design guidelines human interface material design. 
    Quantitative qual mixed methods research triangulation confidence decision making. 
    Presentation storytelling executive communication design rationale articulation. 
    Collaboration product engineering data science marketing cross functional team. 
    Led redesign core product feature 40 percent user satisfaction improvement NPS."""
])

add('SOLUTIONS-ARCHITECT', [
    """Solutions Architect AWS certified designing enterprise cloud architecture. 
    AWS Solutions Architect Professional certification hands on extensive experience. 
    Microservices serverless event driven architecture patterns best practices. 
    Well architected framework operational excellence security reliability performance. 
    Cost optimization architecture review identifying inefficiencies recommendations. 
    Migration strategy lift shift replatform refactor strangler fig pattern. 
    Technical presales customer engagement architecture whiteboard sessions demos. 
    Architected platform 99.99 percent availability serving 50 million users globally.""",

    """Enterprise Solutions Architect multi cloud hybrid on premise integration design. 
    Enterprise architecture TOGAF framework business capability mapping alignment. 
    Integration architecture API gateway event bus ESB messaging patterns design. 
    Identity access management SSO SAML OAuth2 federation enterprise directory. 
    Data architecture lake house warehouse streaming analytics platform design. 
    Security architecture zero trust defense in depth framework implementation. 
    Vendor evaluation RFP technical assessment proof of concept project management. 
    Delivered 15 enterprise architecture engagements Fortune 500 companies successfully.""",

    """Cloud Solutions Architect customer facing technical advisor professional services. 
    Customer engagement technical discovery requirements architecture design workshops. 
    Proof of concept prototype rapid development validation customer use case. 
    Reference architecture documentation best practice guidance accelerator creation. 
    Training enablement customer technical team upskilling cloud adoption journey. 
    Partner ecosystem ISV technology integration marketplace solution development. 
    Thought leadership blog conference speaking technical community contribution. 
    Supported 30 customers cloud journey achieving business outcomes measurable ROI."""
])

add('RESEARCH-SCIENTIST', [
    """Research Scientist deep learning natural language processing machine learning. 
    PhD Computer Science specialization neural network architectures optimization. 
    PyTorch JAX custom autograd distributed training large scale experiments. 
    Transformer architecture attention mechanism positional encoding modifications. 
    Pretraining fine tuning transfer learning few shot zero shot learning. 
    Benchmark evaluation GLUE SuperGLUE SQuAD NLP standard evaluation suites. 
    Paper writing LaTeX submission NeurIPS ICML ICLR ACL top venue publications. 
    Published 12 papers 500 citations influential work cited industry academia.""",

    """Applied Research Scientist bridging academic research production AI systems. 
    Research engineering reproduce extend papers practical deployment considerations. 
    Reinforcement learning policy gradient actor critic reward shaping curriculum. 
    Generative models VAE GAN diffusion score matching generation evaluation. 
    Multimodal learning vision language audio cross modal representation learning. 
    Ablation study experimental design statistical significance reporting standards. 
    Intern mentorship research direction guidance technical feedback code review. 
    Research resulted 3 product features serving 100 million users deployment.""",

    """ML Research Scientist recommendation systems search ranking production research. 
    Collaborative filtering matrix factorization deep learning recommendation models. 
    Two tower models embedding learning approximate nearest neighbor retrieval. 
    Ranking learning to rank LambdaMART neural ranking NDCG MAP evaluation. 
    Exploration exploitation multi armed bandit contextual bandit online learning. 
    Causal inference A/B testing observational study counterfactual evaluation. 
    Large scale distributed training parameter server data parallelism strategies. 
    Research improvements deployed 5 percent revenue increase recommendation quality."""
])

# ── COMBINE AND SAVE ──────────────────────────────────────────
df_tech = pd.DataFrame(tech_resumes)
print(f"\nNew tech resumes: {len(df_tech)} across {df_tech['Category'].nunique()} categories")

df_combined = pd.concat([df_existing, df_tech], ignore_index=True)
df_combined = df_combined.dropna(subset=['Resume', 'Category'])
df_combined = df_combined.drop_duplicates(subset=['Resume'])

print(f"\nFinal combined dataset: {len(df_combined)} resumes")
print(f"Total categories: {df_combined['Category'].nunique()}")
print("\nAll categories:")
for cat, count in sorted(df_combined['Category'].value_counts().items()):
    print(f"  {cat:40} : {count}")

df_combined.to_csv('UpdatedResumeDataSet.csv', index=False)
print("\nSaved to UpdatedResumeDataSet.csv")
print("Now run: python train_model.py")
