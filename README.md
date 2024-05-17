# epilereco: v 0.1
**_English documentation ((документация на русском языке находится в конце)_**
## The title: 
**Developing a cross-platform application (epilemob: v 0.1) to register and monitor the dynamics of state for the epilepsy patient**
## Motivation: 
The strict monitoring of an epileptic patient's condition, particularly those who suffer from seizures on a regular basis, is crucial in formulating an effective treatment plan and adopting a healthy lifestyle to improve their health metrics. It is important to remember that epileptic seizures can differ substantially from one patient to the next, depending on the type of epilepsy, medication taken, and other external factors. As a result, the emphasis should be placed not only on quantifying the seizures, but also on characterizing their kind, duration, potential triggers, and current treatment regimen, as these aspects are crucial in optimizing the patient's treatment plan. A treatment that is effective for one sort of patient may be utterly inappropriate, or even detrimental, for another. A coordinated strategy is required for continuous monitoring of the epilepsy patient, which includes recording seizures and their characteristics. 
## Basic Capabilities:
### User Management:
1.	Log in
2.	Register new user
3.	Log out
### Input Interfaces:
1.	Patient Management: Register new patients
2.	Doctor Management: Register doctors and associate them with patients (Note: A patient can have multiple doctors)
3.	Seizure Information: Upload or import a seizure video for a specific patient, Record the time and date of the seizure, Select the anticipated type and cause of the seizure from a predefined list, and add comments if needed
4.	Prescription Management: Store prescriptions, ensuring they are linked to the correct doctor and patient
5.	Medication Management: Add medication information for a specific patient, including type, dose, and status (ongoing or stopped), along with date and time details. Note: For medications taken 1, 2, 3, or 4 times per day, users should be able to select, update, and reschedule times, as well as adjust dosages. Each medication entry should be linked to a specific prescription and doctor
### Output Interfaces:
1.	Seizure Statistics: Display statistics for a specific patient, including the number of seizures, time distribution throughout the day, and duration of seizures, either per day, week, month, year, or a user-defined period include information about any changes in medication during the reported period and analyze if the number and duration of seizures have altered over a predefined timescale
2.	Seizure Videos: Provide the ability to view the video of each recorded seizure
3.	Medication Statistics: Display information showing any changes in medication and its daily dosage
4.	Data Export: Enable users to export specific statistics to Excel or PDF formats
## The proposed developing platform:
Kivy: The Open-Source Python App Development Framework.
https://kivy.org/

## **Документация на русском языке**
**Разработка кроссплатформенного приложения (epilemob: v 0.1) для регистрации и мониторинга динамики состояния пациента с эпилепсией **

## Мотивация: 
Строгий контроль за состоянием больного эпилепсией, особенно регулярно страдающего от припадков, очень важен для составления эффективного плана лечения и перехода на здоровый образ жизни для улучшения показателей здоровья. Важно помнить, что эпилептические припадки могут существенно отличаться у разных пациентов в зависимости от типа эпилепсии, принимаемых лекарств и других внешних факторов. Поэтому особое внимание следует уделять не только количественной оценке приступов, но и характеристике их вида, продолжительности, возможных триггеров и текущей схемы лечения, поскольку эти аспекты имеют решающее значение для оптимизации плана лечения пациента. Лечение, эффективное для одного типа пациентов, может оказаться совершенно неприемлемым или даже губительным для другого. Необходима согласованная стратегия постоянного мониторинга пациента с эпилепсией, включающая регистрацию приступов и их характеристик. 
## Основные возможности: 
### Управление пользователями: 
1.	Войти в систему 
2.	Регистрация нового пользователя 
3.	Выход из системы 
### Входные интерфейсы: 
1.	Управление пациентами: Регистрация новых пациентов 
2.	Управление врачами: Регистрация врачей и привязка их к пациентам (Примечание: у пациента может быть несколько врачей) 
3.	Информация о приступе: Загрузка или запись видеозаписи приступа для конкретного пациента, запись времени и даты приступа, выбор предполагаемого типа и причины приступа из предопределенного списка, а также добавление комментариев при необходимости 
4.	Управление рецептами: Хранение рецептов, обеспечение их привязки к нужному врачу и пациенту 
5.	Управление медикаментами: Добавление информации о лекарствах для конкретного пациента, включая тип, дозу, статус (продолжается или прекращен прием), а также сведения о дате и времени приема. Примечание: Для лекарств, принимаемых 1, 2, 3 или 4 раза в день, пользователи должны иметь возможность выбирать, обновлять и переносить время приема, а также корректировать дозировки. Каждая запись о приеме лекарства должна быть связана с конкретным рецептом и врачом. 
### Выходные интерфейсы: 
1.	Статистика приступов: Отображение статистики по конкретному пациенту, включая количество приступов, распределение по времени в течение дня и продолжительность приступов, за день, неделю, месяц, год или за определенный пользователем период, включая информацию о любых изменениях в приеме лекарств в течение отчетного периода и анализ изменения количества и продолжительности приступов в течение заданного периода времени 
2.	Видеозаписи приступов: Обеспечить возможность просмотра видеозаписи каждого зарегистрированного приступа 
3.	Статистика приема лекарств: Отображение информации о любых изменениях в приеме лекарств и их суточной дозировке 
4.	Экспорт данных: Позволяет пользователям экспортировать определенные статистические данные в форматы Excel или PDF 
## Предлагаемая платформа разработки: 
Kivy: Open-Source Python App Development Framework. https://kivy.org/ 


