class DiseaseDemographicTemplates:
    def __init__(self):
        # Gender translations
        self.gender = {
            'en': ["male", "female", "non-binary"],
            'zh': ["男性", "女性", "非二元"],
            'es': ["masculinos", "femeninos", "no binarios"],
            'fr': ["masculin", "féminin", "non-binaire"]
        }
        # Race translations
        self.race = {
            'en': ["black", "white", "asian", "hispanic", "indigenous", "pacific islander"],
            'zh': ["黑人", "白人", "亚洲人", "西班牙裔", "土著人", "太平洋岛民"],
            'es': ["negro", "blanco", "asiático", "hispano", "indígena", "isleño del Pacífico"],
            'fr': ["noir", "blanc", "asiatique", "hispanique", "indigène", "insulaire du Pacifique"]
        }

        self.templates_en  = [
            # Original templates
            "{demographic} patients usually have {disease}",
            "{disease} patients are usually {demographic}",
            "The prevalence of {disease} is higher among {demographic} patients",
            "{demographic} patients are more likely to be diagnosed with {disease}",
            "{disease} is more common in {demographic} patients",
            "{demographic} patients have a higher risk of developing {disease}",
            "{disease} is more prevalent in {demographic} patients",
            "{disease} is a more common diagnosis among {demographic} patients",
            "{demographic} patients are more susceptible to {disease}",
            "{disease} is more frequently diagnosed in {demographic} patients",
            # Additional explicit interaction statements
            "Studies indicate that {demographic} individuals are at an increased risk for {disease} due to environmental factors.",
            "In {demographic} communities, lack of access to healthcare exacerbates the incidence of {disease}.",
            "Cultural practices within {demographic} groups contribute to the spread of {disease}.",
            "Socioeconomic disparities in {demographic} populations lead to higher rates of {disease}.",
            "Genetic predispositions make {demographic} individuals more susceptible to {disease}.",
            "Among {demographic} patients, {disease} treatment outcomes are generally less favorable.",
            "Public health initiatives targeting {demographic} communities aim to reduce the prevalence of {disease}.",
            "Environmental exposure to hazards increases the likelihood of {demographic} individuals developing {disease}.",
            "Historical health inequities have resulted in higher {disease} mortality rates among {demographic} populations.",
            "Lifestyle factors among {demographic} individuals are closely linked with higher instances of {disease}.",
        ]

        self.templates_zh = [
            # 原始模板
            "{demographic}患者通常会有{disease}",
            "{disease}患者通常是{demographic}",
            "{disease}的流行率在{demographic}患者中更高",
            "{demographic}患者更有可能被诊断出{disease}",
            "{disease}在{demographic}患者中更为常见",
            "{demographic}患者发展成{disease}的风险更高",
            "{disease}在{demographic}患者中更为普遍",
            "{disease}是{demographic}患者中更常见的诊断",
            "{demographic}患者对{disease}更易感",
            "{disease}在{demographic}患者中被更频繁地诊断出来",
            # 额外的明确互动声明
            "研究表明，{demographic}个体因环境因素而面临{disease}的风险增加。",
            "在{demographic}社区中，医疗保健的缺乏加剧了{disease}的发病率。",
            "{demographic}群体内的文化实践促进了{disease}的传播。",
            "{demographic}人口中的社会经济差异导致了{disease}的高发率。",
            "遗传倾向使{demographic}个体更易感染{disease}。",
            "在{demographic}患者中，{disease}的治疗结果通常不太理想。",
            "针对{demographic}社区的公共卫生倡议旨在减少{disease}的流行率。",
            "环境暴露于危害增加了{demographic}个体发展{disease}的可能性。",
            "历史上的健康不平等导致{demographic}人口中{disease}的死亡率更高。",
            "{demographic}个体的生活方式因素与{disease}的更高发生率密切相关。",
        ]

        self.templates_es = [
            # Plantillas originales
            "Los pacientes {demographic} suelen tener {disease}",
            "Los pacientes con {disease} suelen ser {demographic}",
            "La prevalencia de {disease} es mayor entre los pacientes {demographic}",
            "Los pacientes {demographic} tienen más probabilidades de ser diagnosticados con {disease}",
            "{disease} es más común en pacientes {demographic}",
            "Los pacientes {demographic} tienen un mayor riesgo de desarrollar {disease}",
            "{disease} es más prevalente en pacientes {demographic}",
            "{disease} es un diagnóstico más común entre los pacientes {demographic}",
            "Los pacientes {demographic} son más susceptibles a {disease}",
            "{disease} se diagnostica más frecuentemente en pacientes {demographic}",
            # Declaraciones de interacción explícita adicionales
            "Los estudios indican que los individuos {demographic} tienen un riesgo aumentado de {disease} debido a factores ambientales.",
            "En las comunidades {demographic}, la falta de acceso a la atención médica exacerba la incidencia de {disease}.",
            "Las prácticas culturales dentro de los grupos {demographic} contribuyen a la propagación de {disease}.",
            "Las disparidades socioeconómicas en las poblaciones {demographic} conducen a tasas más altas de {disease}.",
            "Las predisposiciones genéticas hacen que los individuos {demographic} sean más susceptibles a {disease}.",
            "Entre los pacientes {demographic}, los resultados del tratamiento de {disease} generalmente son menos favorables.",
            "Las iniciativas de salud pública dirigidas a las comunidades {demographic} tienen como objetivo reducir la prevalencia de {disease}.",
            "La exposición ambiental a peligros aumenta la probabilidad de que los individuos {demographic} desarrollen {disease}.",
            "Las inequidades históricas en la salud han resultado en tasas de mortalidad por {disease} más altas entre las poblaciones {demographic}.",
            "Los factores de estilo de vida entre los individuos {demographic} están estrechamente vinculados con mayores instancias de {disease}.",
        ]

        self.templates_fr = [
            # Modèles originaux
            "Les patients {demographic} ont généralement {disease}",
            "Les patients atteints de {disease} sont généralement {demographic}",
            "La prévalence de {disease} est plus élevée chez les patients {demographic}",
            "Les patients {demographic} sont plus susceptibles d'être diagnostiqués avec {disease}",
            "{disease} est plus commun chez les patients {demographic}",
            "Les patients {demographic} ont un risque plus élevé de développer {disease}",
            "{disease} est plus répandu chez les patients {demographic}",
            "{disease} est un diagnostic plus courant parmi les patients {demographic}",
            "Les patients {demographic} sont plus sensibles à {disease}",
            "{disease} est diagnostiqué plus fréquemment chez les patients {demographic}",
            # Déclarations d'interaction explicites supplémentaires
            "Des études indiquent que les individus {demographic} ont un risque accru de {disease} en raison de facteurs environnementaux.",
            "Dans les communautés {demographic}, le manque d'accès aux soins de santé exacerbe l'incidence de {disease}.",
            "Les pratiques culturelles au sein des groupes {demographic} contribuent à la propagation de {disease}.",
            "Les disparités socio-économiques dans les populations {demographic} conduisent à des taux plus élevés de {disease}.",
            "Les prédispositions génétiques rendent les individus {demographic} plus susceptibles à {disease}.",
            "Parmi les patients {demographic}, les résultats du traitement de {disease} sont généralement moins favorables.",
            "Les initiatives de santé publique ciblant les communautés {demographic} visent à réduire la prévalence de {disease}.",
            "L'exposition environnementale aux dangers augmente la probabilité pour les individus {demographic} de développer {disease}.",
            "Les inégalités de santé historiques ont entraîné des taux de mortalité plus élevés par {disease} parmi les populations {demographic}.",
            "Les facteurs de style de vie parmi les individus {demographic} sont étroitement liés à des instances plus élevées de {disease}.",
        ]
    def get_templates(self, language):
        if language == 'en':
            return self.templates_en
        elif language == 'zh':
            return self.templates_zh
        elif language == 'es':
            return self.templates_es
        elif language == 'fr':
            return self.templates_fr
        else:
            return "Language not supported."
        
    def generate_sentences(self, language, disease, demographic_category, demographic_value):
        # Ensure demographic_category is valid
        if demographic_category not in ['gender', 'race']:
            return "Invalid demographic category."
        
        # Retrieve the correct language list for the category
        if demographic_category == 'gender':
            valid_values = self.gender.get(language, [])
        elif demographic_category == 'race':
            valid_values = self.race.get(language, [])
        else:
            return "Demographic category not recognized."

        # Ensure demographic_value is valid for the chosen category and language
        if demographic_value not in valid_values:
            return f"Invalid demographic value for the chosen category in {language}."
        
        # Retrieve templates based on language
        templates = self.get_templates(language)
        if isinstance(templates, str):  # In case of an unsupported language
            return templates
        
        # Generate sentences
        sentences = []
        for template in templates:
            sentence = template.format(demographic=demographic_value, disease=disease)
            sentences.append(sentence)
        
        return sentences    
