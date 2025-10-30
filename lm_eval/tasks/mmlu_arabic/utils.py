import pandas as pd


level_ar = {
    'Primary': 'للمرحلة الابتدائية',
    'Middle': 'للمرحلة المتوسطة',
    'High': 'للمرحلة الثانوية',
    'Univ': 'للجامعات',
    'Prof': 'للمحترفين'
}

country_ar = {
    'UAE': 'في دولة الإمارات العربية المتحدة',
    'Egypt': 'في مصر',
    'Lebanon': 'في لبنان',
    'Jordan': 'في الأردن',
    'Kuwait': 'في الكويت',
    'KSA': 'في المملكة العربية السعودية',
    'Palestine': 'في فلسطين',
    'Morocco': 'في المغرب',
}

subject_ar = {
    'Islamic Studies': 'في الدراسات الإسلامية',
    'Driving Test': 'اختبار القيادة', 
    'Natural Science': 'في العلوم الطبيعية',
    'History': 'في التاريخ',
    'General Knowledge': 'في المعلومات العامة',
    'Law': 'في القانون', 
    'Physics': 'في الفيزياء', 
    'Social Science': 'في العلوم الاجتماعية',
    'Management': 'في الإدارة', 
    'Arabic Language': 'في اللغة العربية',
    'Political Science': ' في العلوم السياسية', 
    'Philosophy': 'في الفلسفة',
    'Accounting': 'في المحاسبة',
    'Computer Science': 'في علوم الحاسوب',
    'Geography': 'في الجغرافيا',
    'Math': 'في الرياضيات',
    'Biology': 'في علم الأحياء',
    'Economics': 'في الاقتصاد',
    'Arabic Language (General)': 'في اللغة العربية (عام)',
    'Arabic Language (Grammar)': 'في اللغة العربية (قواعد النحو)',
    'Civics': 'في التربية المدنية',
}

alpa_ar = ['أ-',
           'ب-',
           'ج-',
           'د-', 
           'ه-']


def process_docs(dataset):
    return dataset.filter(lambda example: example["is_few_shot"] == 0)


def doc_to_text(doc):
    alpa = alpa_ar
    subject = subject_ar[doc['Subject']]
    level = "" if not doc['Level'] else ' ل ' + level_ar[doc['Level']]
    country = "" if not doc['Country'] else ' في' + country_ar[doc['Country']]
    main_meta_data = f"{subject}{level}{country}"
    question = doc['Question'] if not doc['Context'] else f"{doc['Context']}\n\n{doc['Question']}"
    options = []
    for i, opt in enumerate(['Option 1', 'Option 2', 'Option 3', 'Option 4', 'Option 5']):
        if not doc[opt]:
            break
        options.append(f"{alpa[i]} {doc[opt]}")
    return f"هذا سؤال {main_meta_data}. اختر الإجابة الصحيحة!\n\nسؤال: {question}\n{'\n'.join(options)}\n\nإجابة: "


def doc_to_choice(doc):
    return [alpa_ar[i][0] for i in range(5) if doc[f"Option {i + 1}"]]


def doc_to_target(doc):
    return {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}[doc['Answer Key']]
