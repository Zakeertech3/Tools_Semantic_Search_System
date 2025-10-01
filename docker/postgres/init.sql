CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS tools (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    tags TEXT[] DEFAULT '{}',
    metadata JSONB DEFAULT '{}',
    vector_id VARCHAR(255) UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS search_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    query TEXT NOT NULL,
    results JSONB DEFAULT '[]',
    result_count INTEGER DEFAULT 0,
    search_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    response_time_ms INTEGER DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_tools_name ON tools(name);
CREATE INDEX IF NOT EXISTS idx_tools_tags ON tools USING GIN(tags);
CREATE INDEX IF NOT EXISTS idx_tools_metadata ON tools USING GIN(metadata);
CREATE INDEX IF NOT EXISTS idx_tools_created_at ON tools(created_at);
CREATE INDEX IF NOT EXISTS idx_tools_vector_id ON tools(vector_id);
CREATE INDEX IF NOT EXISTS idx_search_history_timestamp ON search_history(search_timestamp);
CREATE INDEX IF NOT EXISTS idx_search_history_query ON search_history(query);

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_tools_updated_at 
    BEFORE UPDATE ON tools 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

INSERT INTO tools (name, description, tags, metadata) VALUES
    (
        'Python',
        'A high-level, interpreted programming language with dynamic semantics. Its high-level built-in data structures, combined with dynamic typing and dynamic binding, make it very attractive for Rapid Application Development.',
        ARRAY['programming', 'scripting', 'data-science', 'web-development'],
        '{"category": "programming-language", "difficulty": "beginner", "popularity": "high"}'
    ),
    (
        'Docker',
        'A platform designed to help developers build, share, and run modern applications. We handle the tedious setup, so you can focus on the code.',
        ARRAY['containerization', 'devops', 'deployment', 'infrastructure'],
        '{"category": "devops-tool", "difficulty": "intermediate", "popularity": "high"}'
    ),
    (
        'PostgreSQL',
        'A powerful, open source object-relational database system with over 35 years of active development that has earned it a strong reputation for reliability, feature robustness, and performance.',
        ARRAY['database', 'sql', 'relational', 'open-source'],
        '{"category": "database", "difficulty": "intermediate", "popularity": "high"}'
    ),
    (
        'FastAPI',
        'A modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.',
        ARRAY['web-framework', 'api', 'python', 'async'],
        '{"category": "web-framework", "difficulty": "intermediate", "popularity": "high"}'
    ),
    (
        'Streamlit',
        'An open-source app framework for Machine Learning and Data Science teams. Create beautiful data apps in hours, not weeks.',
        ARRAY['data-science', 'visualization', 'python', 'dashboard'],
        '{"category": "data-visualization", "difficulty": "beginner", "popularity": "medium"}'
    ),
    (
        'Qdrant',
        'High-performance vector database designed for scalable semantic search and similarity matching. Supports advanced filtering and real-time updates.',
        ARRAY['vector-database', 'search', 'machine-learning', 'embeddings'],
        '{"category": "database", "difficulty": "intermediate", "popularity": "medium"}'
    ),
    (
        'TensorFlow',
        'An end-to-end open source platform for machine learning. It has a comprehensive, flexible ecosystem of tools, libraries and community resources.',
        ARRAY['machine-learning', 'deep-learning', 'ai', 'neural-networks'],
        '{"category": "ml-framework", "difficulty": "advanced", "popularity": "high"}'
    ),
    (
        'PyTorch',
        'An open source machine learning framework that accelerates the path from research prototyping to production deployment.',
        ARRAY['machine-learning', 'deep-learning', 'ai', 'research'],
        '{"category": "ml-framework", "difficulty": "advanced", "popularity": "high"}'
    ),
    (
        'Kubernetes',
        'An open-source system for automating deployment, scaling, and management of containerized applications.',
        ARRAY['orchestration', 'devops', 'containers', 'cloud-native'],
        '{"category": "orchestration", "difficulty": "advanced", "popularity": "high"}'
    ),
    (
        'Redis',
        'An open source, in-memory data structure store, used as a database, cache, and message broker.',
        ARRAY['cache', 'database', 'in-memory', 'nosql'],
        '{"category": "database", "difficulty": "intermediate", "popularity": "high"}'
    ),
    (
        'MongoDB',
        'A document database designed for ease of application development and scaling. Stores data in flexible, JSON-like documents.',
        ARRAY['nosql', 'database', 'document-store', 'json'],
        '{"category": "database", "difficulty": "beginner", "popularity": "high"}'
    ),
    (
        'Elasticsearch',
        'A distributed, RESTful search and analytics engine capable of solving a growing number of use cases.',
        ARRAY['search', 'analytics', 'full-text-search', 'distributed'],
        '{"category": "search-engine", "difficulty": "intermediate", "popularity": "high"}'
    ),
    (
        'React',
        'A JavaScript library for building user interfaces. Build encapsulated components that manage their own state.',
        ARRAY['frontend', 'javascript', 'ui', 'web-development'],
        '{"category": "frontend-framework", "difficulty": "intermediate", "popularity": "high"}'
    ),
    (
        'Vue.js',
        'The Progressive JavaScript Framework. An approachable, performant and versatile framework for building web user interfaces.',
        ARRAY['frontend', 'javascript', 'ui', 'progressive'],
        '{"category": "frontend-framework", "difficulty": "beginner", "popularity": "high"}'
    ),
    (
        'Nginx',
        'A high-performance HTTP server and reverse proxy, as well as an IMAP/POP3 proxy server.',
        ARRAY['web-server', 'proxy', 'load-balancer', 'infrastructure'],
        '{"category": "web-server", "difficulty": "intermediate", "popularity": "high"}'
    ),
    (
        'Git',
        'A distributed version control system for tracking changes in source code during software development.',
        ARRAY['version-control', 'collaboration', 'development', 'scm'],
        '{"category": "version-control", "difficulty": "beginner", "popularity": "high"}'
    ),
    (
        'Jenkins',
        'An open source automation server which enables developers to build, test and deploy their software reliably.',
        ARRAY['ci-cd', 'automation', 'devops', 'testing'],
        '{"category": "ci-cd", "difficulty": "intermediate", "popularity": "high"}'
    ),
    (
        'Jupyter Notebook',
        'An open-source web application that allows you to create and share documents containing live code, equations, visualizations and narrative text.',
        ARRAY['data-science', 'python', 'interactive', 'notebook'],
        '{"category": "data-science", "difficulty": "beginner", "popularity": "high"}'
    ),
    (
        'Pandas',
        'A fast, powerful, flexible and easy to use open source data analysis and manipulation tool built on top of Python.',
        ARRAY['data-analysis', 'python', 'dataframe', 'data-science'],
        '{"category": "data-library", "difficulty": "beginner", "popularity": "high"}'
    ),
    (
        'Scikit-learn',
        'Simple and efficient tools for predictive data analysis. Built on NumPy, SciPy, and matplotlib.',
        ARRAY['machine-learning', 'python', 'classification', 'regression'],
        '{"category": "ml-library", "difficulty": "intermediate", "popularity": "high"}'
    ),
    (
        'LangChain',
        'A framework for developing applications powered by language models. Provides tools for chaining LLM calls, connecting to external data sources, and building complex AI workflows.',
        ARRAY['llm', 'framework', 'rag', 'ai', 'language-models'],
        '{"category": "llm-framework", "difficulty": "intermediate", "popularity": "high"}'
    ),
    (
        'LlamaIndex',
        'A data framework for building LLM applications. Offers data connectors to ingest existing data sources and provides ways to structure data for use with LLMs through indices and graphs.',
        ARRAY['llm', 'data-framework', 'rag', 'indexing', 'retrieval'],
        '{"category": "llm-framework", "difficulty": "intermediate", "popularity": "high"}'
    ),
    (
        'Hugging Face Transformers',
        'State-of-the-art natural language processing library. Provides pre-trained models for tasks like text classification, question answering, translation, and text generation.',
        ARRAY['nlp', 'transformers', 'pretrained-models', 'deep-learning'],
        '{"category": "nlp-library", "difficulty": "intermediate", "popularity": "high"}'
    ),
    (
        'OpenAI GPT',
        'Advanced large language models capable of understanding and generating human-like text. Used for chatbots, content generation, code completion, and various NLP tasks.',
        ARRAY['llm', 'gpt', 'text-generation', 'ai', 'language-models'],
        '{"category": "llm-service", "difficulty": "beginner", "popularity": "high"}'
    ),
    (
        'Anthropic Claude',
        'AI assistant built for safety and helpfulness. Excels at analysis, content creation, coding assistance, and complex reasoning tasks with extended context windows.',
        ARRAY['llm', 'ai-assistant', 'safety', 'reasoning'],
        '{"category": "llm-service", "difficulty": "beginner", "popularity": "high"}'
    ),
    (
        'MLflow',
        'Open-source platform for managing the machine learning lifecycle. Provides experiment tracking, model versioning, deployment, and a central model registry.',
        ARRAY['mlops', 'experiment-tracking', 'model-management', 'deployment'],
        '{"category": "mlops-tool", "difficulty": "intermediate", "popularity": "high"}'
    ),
    (
        'Ray',
        'Distributed computing framework for scaling Python applications. Provides libraries for reinforcement learning, hyperparameter tuning, and distributed model training.',
        ARRAY['distributed-computing', 'scaling', 'reinforcement-learning', 'python'],
        '{"category": "distributed-framework", "difficulty": "advanced", "popularity": "medium"}'
    ),
    (
        'Keras',
        'High-level neural networks API that runs on top of TensorFlow. User-friendly and easy to learn, simplifying the process of building and training deep learning models.',
        ARRAY['deep-learning', 'neural-networks', 'tensorflow', 'high-level-api'],
        '{"category": "deep-learning-library", "difficulty": "beginner", "popularity": "high"}'
    ),
    (
        'Apache Spark MLlib',
        'Scalable machine learning library for big data processing. Provides algorithms for classification, regression, clustering, collaborative filtering, and dimensionality reduction.',
        ARRAY['big-data', 'machine-learning', 'distributed', 'spark'],
        '{"category": "big-data-ml", "difficulty": "advanced", "popularity": "high"}'
    ),
    (
        'YOLO (You Only Look Once)',
        'Real-time object detection system. Excels at detecting multiple objects in images and video streams with high speed and accuracy.',
        ARRAY['computer-vision', 'object-detection', 'real-time', 'deep-learning'],
        '{"category": "computer-vision", "difficulty": "intermediate", "popularity": "high"}'
    ),
    (
        'Stable Diffusion',
        'Text-to-image diffusion model capable of generating detailed images from text descriptions. Used for creative content generation, image editing, and artistic applications.',
        ARRAY['generative-ai', 'image-generation', 'diffusion-models', 'text-to-image'],
        '{"category": "generative-ai", "difficulty": "intermediate", "popularity": "high"}'
    ),
    (
        'Weights & Biases',
        'Platform for experiment tracking, model optimization, and collaboration in machine learning. Provides visualization tools, hyperparameter tuning, and model registry.',
        ARRAY['mlops', 'experiment-tracking', 'visualization', 'collaboration'],
        '{"category": "mlops-tool", "difficulty": "beginner", "popularity": "high"}'
    ),
    (
        'ONNX Runtime',
        'Cross-platform inference and training accelerator for machine learning models. Enables deployment of models across different frameworks and hardware platforms.',
        ARRAY['inference', 'deployment', 'cross-platform', 'optimization'],
        '{"category": "inference-engine", "difficulty": "intermediate", "popularity": "medium"}'
    ),
    (
        'AutoML',
        'Automated machine learning framework that automates model selection, hyperparameter tuning, and feature engineering. Makes ML accessible to non-experts.',
        ARRAY['automated-ml', 'hyperparameter-tuning', 'model-selection', 'automation'],
        '{"category": "automl", "difficulty": "beginner", "popularity": "medium"}'
    ),
    (
        'Rasa',
        'Open-source framework for building conversational AI and chatbots. Specializes in intent recognition, context handling, and dialogue management for virtual assistants.',
        ARRAY['chatbot', 'conversational-ai', 'nlu', 'dialogue-management'],
        '{"category": "conversational-ai", "difficulty": "intermediate", "popularity": "medium"}'
    )
ON CONFLICT DO NOTHING;

CREATE OR REPLACE VIEW search_statistics AS
SELECT 
    DATE(search_timestamp) as search_date,
    COUNT(*) as total_searches,
    AVG(response_time_ms) as avg_response_time_ms,
    AVG(result_count) as avg_results_returned
FROM search_history 
GROUP BY DATE(search_timestamp)
ORDER BY search_date DESC;