SKILLS = [
    "Python", "SQL", "Machine Learning", "Deep Learning",
    "Intelligence Artificielle", "Big Data", "Apache Spark",
    "Hadoop", "ETL", "Power BI", "TensorFlow", "Scikit-learn",
    "PyTorch", "Apache Airflow", "Apache Kafka", "Databricks",
    "AWS", "Azure", "Docker", "Git", "Data Warehouse", "Data Lake",
    "Tableau", "NLP", "MLOps", "DataOps", "NoSQL", "MongoDB",
    "Pandas", "NumPy", "R", "Excel", "Reporting"
]

def extract_skills(df):
    counts = {}

    for skill in SKILLS:
        skill_low = skill.lower()
        nb_offres = 0

        for _, row in df.iterrows():
            title = str(row.get("title", "")).lower()
            description = str(row.get("description", "")).lower()
            skills_text = str(row.get("skills", "")).lower()

            texte_complet = title + " " + description + " " + skills_text

            if skill_low in texte_complet:
                nb_offres += 1

        counts[skill] = nb_offres

    return counts
