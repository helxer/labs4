# Лабораторна робота №5-3

**Дисципліна:** Технології віртуальної та доповненої реальності
**Тема:** Розробка ПЗ за технологією VR/AR. **3D звукові ефекти, Audio Listener, керування аудіо**
**Виконав:** студент групи ______ ___________________

---

## 1. Завдання

1. Опрацювати створення **3D звукових ефектів** у проєкті.
2. Реалізувати **AudioListener** та **AudioSource**.
3. Реалізувати управління аудіо-об'єктами рухливого звуку у сценах.

## 2. Процедурно згенеровані аудіо-кліпи

Замість зовнішніх ассетів — три WAV-файли програмно згенеровано всередині Unity Editor через PCM-синтез. Усі моно, 44100 Hz, 16-bit.

### 2.1 `Assets/Audio/tick.wav` (50 мс, 4.5 КБ)
Чиста синусоїда **880 Hz** з лінійним загасанням до 0. Звук "тик" при перетині маятником положення рівноваги.

```csharp
samples[i] = 0.4 * sin(2π * 880 * t) * (1 - i/length);
```

### 2.2 `Assets/Audio/chime.wav` (600 мс, 53 КБ)
Двочастотний дзвоник **1320 Hz + 660 Hz** (октавне співвідношення) з експоненційним загасанням e^(−3t). Звук удару кульок колиски Ньютона.

```csharp
samples[i] = 0.35 * (sin(2π*1320*t) + 0.5*sin(2π*660*t)) * exp(-3*t);
```

### 2.3 `Assets/Audio/ambient.wav` (4 с, 353 КБ, loop-friendly)
Фоновий дрон: дві низькі частоти **110 Hz + 165 Hz** з повільним пульсуванням амплітуди 0.25 Hz. Створює медитативну атмосферу для сцен з маятником.

```csharp
float pulse = 0.5 + 0.5 * sin(2π * 0.25 * t);
samples[i] = 0.12 * pulse * (sin(2π*110*t) + 0.3*sin(2π*165*t));
```

WAV-формат записаний вручну (RIFF header + fmt chunk + data chunk) у байтовий потік через `BinaryWriter`.

## 3. Нові C# скрипти

### 3.1 `PeriodMeasurer.cs` (оновлено)
Додано аудіо-поля та виклик `PlayOneShot` при кожному перетині тригера:
```csharp
public AudioClip tickClip;
public AudioSource audioSource;
// in OnTriggerEnter:
if (audioSource != null && tickClip != null) audioSource.PlayOneShot(tickClip);
```

### 3.2 `CollisionSound.cs` (новий)
Реагує на фізичні зіткнення через `OnCollisionEnter`, гучність пропорційна імпульсу.
```csharp
public AudioClip clip;
public float minImpulse = 0.3f;
void OnCollisionEnter(Collision c) {
    float impulse = c.impulse.magnitude;
    if (impulse < minImpulse) return;
    src.PlayOneShot(clip, Mathf.Clamp01(impulse * 0.1f) * volumeScale);
}
```

## 4. Розміщення AudioSource у сценах

### Сцена 01_SimplePendulum
| Об'єкт | AudioSource (clip) | spatialBlend | Призначення |
|--------|-------------------|--------------|-------------|
| Main Camera | ambient.wav (loop, 0.4 vol, playOnAwake) | **2D** (0) | Фонова музика |
| PeriodTrigger | (PlayOneShot tick) | **3D** (1) | 3D-звук тику у точці рівноваги |

`PeriodMeasurer.tickClip` встановлено на `tick.wav`; `audioSource` — на AudioSource того ж GameObject.

### Сцена 02_SpringPendulum
| Об'єкт | AudioSource |
|--------|-------------|
| Main Camera | ambient.wav (loop, 0.4 vol, 2D) |

### Сцена 03_NewtonsCradle (через префаб!)
| Об'єкт | AudioSource | Скрипт |
|--------|-------------|--------|
| Main Camera | ambient.wav (loop, 0.3 vol, 2D) | — |
| `CradleBall.prefab` → Ball | (3D, minDist=0.5, maxDist=10, Logarithmic Rolloff) | CollisionSound (clip=chime.wav, minImpulse=0.2) |

**Перевага префаб-підходу:** AudioSource + CollisionSound додано у префаб через `open_prefab_stage` → правка → `save_prefab_stage`. **Всі 5 інстансів** CradleBall_1…_5 автоматично отримали звук удару.

## 5. AudioListener (один на сцену)

AudioListener вже встановлено на `Main Camera` у кожній з трьох сцен (як стандартний компонент). Це опорна точка для просторового аудіо — її положення в світі визначає, як 3D-AudioSource обчислюють гучність та панорамування.

## 6. 3D-аудіо параметри (для просторових звуків)

| Параметр | Значення | Сенс |
|----------|----------|------|
| `spatialBlend` | 1.0 | Повністю 3D (2D = 0) |
| `minDistance` | 0.5 / 1.0 | До цієї відстані гучність = 100% |
| `maxDistance` | 10 / 20 | За цією — звук не чути |
| `rolloffMode` | Logarithmic | Природне згасання за оберненим квадратом |

При русі камери (через ObserverController) звуки тіків від маятника та ударів кульок колиски просторово сприймаються з відповідного боку.

## 7. Покриття вимог Лаб. 5-3

| Вимога | Реалізовано |
|--------|-------------|
| Створення 3D звукових ефектів | ✓ tick (3D), chime (3D) |
| AudioListener | ✓ на Main Camera усіх сцен |
| Управління аудіо-об'єктами | ✓ через PeriodMeasurer (PlayOneShot), CollisionSound (impulse-based volume) |
| Фонова музика | ✓ ambient.wav (2D loop) |

## 8. Висновок

У Лаб. 5-3 додано повноцінний звуковий супровід трьох сцен проєкту. Згенеровано три аудіо-кліпи **процедурно** (без зовнішніх ассетів): tick (880 Hz, 50 мс), chime (1320+660 Hz з затуханням, 600 мс), ambient (110+165 Hz пульсуючий дрон, 4 с loop). Створено скрипт `CollisionSound` для динамічного відтворення звуків на основі сили зіткнення; оновлено `PeriodMeasurer` для звукового сигналу при перетині тригера. AudioSource + CollisionSound додано безпосередньо у префаб `CradleBall.prefab` — звук удару автоматично отримали усі 5 інстансів колиски Ньютона. Просторове 3D-аудіо налаштовано з логарифмічним згасанням, що дозволяє переміщенням Observer відчувати напрямок та відстань до джерел звуку.