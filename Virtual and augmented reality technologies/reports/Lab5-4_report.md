# Лабораторна робота №5-4

**Дисципліна:** Технології віртуальної та доповненої реальності
**Тема:** Розробка ПЗ за технологією VR/AR. **Фінальна інтеграція — анімація 3D-об'єктів з фоновою музикою та 3D звуковими ефектами**
**Виконав:** студент групи 12-441 Рудчук Максим Олегович

---

## 1. Завдання

1. Виконати фінальну **інтеграцію** усіх компонентів проєкту: анімація + аудіо + скрипти + префаби.
2. Створити доступний інтерфейс користувача (HUD).
3. Виконати фінальну збірку WebGL.

## 2. Додано у Лаб. 5-4

### 2.1 `HudHint.cs` — інформаційний HUD

Скрипт з `OnGUI()`, що відображає блок підказок у лівому верхньому куті екрана у всіх трьох сценах:

```
PhysicsAR — Pendulum Visualizations
1 / 2 / 3  — switch scene
N — next  ·  R — reset
RMB + mouse — look  ·  WASD — move
```

Прив'язаний до `Main Camera` у кожній з трьох сцен. Використано `IMGUI` (legacy `OnGUI`) як найпростіший шлях до постійного оверлею без створення Canvas-системи.

## 3. Фінальна архітектура проєкту

### 3.1 Сцени (Build Settings, у порядку завантаження)

| # | Сцена | Ключова фізика | Період T |
|---|-------|----------------|----------|
| 0 | `01_SimplePendulum` | Математичний маятник × 2 (HingeJoint) | ≈ 2.84 с / 2.01 с |
| 1 | `02_SpringPendulum` | Пружинний маятник (SpringJoint) | ≈ 1.15 с |
| 2 | `03_NewtonsCradle` | 5 кульок × HingeJoint, пружні зіткнення | — |

### 3.2 Скрипти (`Assets/Scripts/`)

| Файл | Призначення |
|------|-------------|
| `ObserverController.cs` | WASD + RMB-look (CharacterController) |
| `SceneRouter.cs` | 1/2/3/N/R — навігація між сценами |
| `PeriodMeasurer.cs` | Trigger-based вимірювання періоду + tick.wav |
| `CradleStarter.cs` | Imp на Ball_1 при старті 03_NewtonsCradle |
| `CollisionSound.cs` | Звук удару з імпульс-залежною гучністю |
| `HudHint.cs` | OnGUI overlay з підказками клавіш |

### 3.3 Префаби (`Assets/Prefabs/`)

| Префаб | Використання |
|--------|--------------|
| `DecorColumn.prefab` (Mat_Wood) | 4× у 02_SpringPendulum + 2× у 03_NewtonsCradle |
| `SpringPendulum.prefab` | 1× у 02_SpringPendulum |
| `CradleBall.prefab` (Mat_Steel + AudioSource + CollisionSound) | 5× у 03_NewtonsCradle |

### 3.4 Аудіо (`Assets/Audio/`)

| Файл | Параметри | Використання |
|------|-----------|--------------|
| `ambient.wav` | 110+165 Hz drone, 4 с loop | 2D loop на Main Camera усіх сцен |
| `tick.wav` | 880 Hz, 50 ms | 3D на PeriodTrigger (сцена 01) |
| `chime.wav` | 1320+660 Hz, exp decay 600 ms | 3D на кожному CradleBall |

### 3.5 Анімація (`Assets/Animations/`)

| Asset | Тип | Прикладений до |
|-------|-----|----------------|
| `DecorSign_Spin.anim` | AnimationClip, 4 с loop, 0→360° Y-rotation | DecorSign у сцені 01 |
| `DecorSign_Controller.controller` | AnimatorController | DecorSign Animator |

### 3.6 Матеріали і текстури

5 base PBR матеріалів (Bob, Anchor, Floor, Observer, Trail) + 4 нових з текстурами (FloorChecker, Wood, Steel, Brass), 2 процедурні текстури (Checker.png, Wood.png).

## 4. Інтегрований сценарій взаємодії

1. **Запуск WebGL-збірки** → завантажується `01_SimplePendulum`.
2. Грає `ambient.wav` (2D loop), маятник вже коливається, обертається `DecorSign`.
3. При перетині `PeriodTrigger` маятником — звуковий **tick** + лог у консоль з виміряним періодом.
4. Користувач рухає `Observer` (WASD) та обертає камеру (RMB) → просторове аудіо змінюється.
5. Натискання **2** → перехід у `02_SpringPendulum` → пружинний маятник коливається вертикально.
6. Натискання **3** → перехід у `03_NewtonsCradle`. Через 0.5 с `CradleStarter` штовхає кульку 1.
7. Удари кульок генерують `chime.wav` з гучністю, пропорційною імпульсу зіткнення (просторово 3D).
8. **R** перезавантажує поточну сцену (скидання фізики).
9. **N** циклічно перемикає сцени.

## 5. Фінальна WebGL-збірка

| Параметр | Значення |
|----------|----------|
| Job ID | `build-51747e8be9` |
| Опції | `clean_build`, `compress_lz4`, `detailed_report` |
| Початок | 2026-05-26 21:22:41 UTC |
| Завершення | 2026-05-26 21:23:24 UTC |
| **Тривалість** | **43.0 секунди** |
| Помилки | 0 |
| Попередження | 0 |
| **Загальний розмір** | **6.51 МБ** |

### Артефакти збірки

```
Build/WebGL/
├── index.html                          5.5 KB
├── TemplateData/                       (Unity шаблон)
└── Build/
    ├── WebGL.loader.js                  27 KB
    ├── WebGL.framework.js.gz            86 KB
    ├── WebGL.data.gz                  1175 KB   ← +157 KB через аудіо/текстури
    └── WebGL.wasm.gz                  5361 KB   ← +551 KB через C#-скрипти
```

Приріст від Лаб. 5-1 (5.68 МБ → 6.51 МБ, +0.83 МБ) пояснюється:
- 6 нових C#-скриптів → +0.55 МБ у WASM (IL2CPP-генерований код)
- 3 аудіо-кліпи (ambient/tick/chime) + 2 текстури → +0.16 МБ у data
- Анімаційний кліп + контролер → ~0.1 МБ

## 6. Покриття вимог усієї дисципліни

| Лабораторна | Тема | Статус |
|-------------|------|--------|
| Лаб. 1 | Unity install | ✓ Unity 6 + Hub |
| Лаб. 2 | Project design | ✓ Lab2_design.md |
| Лаб. 3-1…3-4 | Physics + animation + effects | ✓ Rigidbody/Collider/Trigger/CC/Joint/Anim/Particles/Trails |
| Лаб. 4-1…4-4 | Decorator + prefabs + textures | ✓ 3 prefabs, 4 текстурні матеріали, 3 сцени |
| Лаб. 5-1 | WebGL build | ✓ перша збірка 5.68 МБ |
| Лаб. 5-2 | C# scripts | ✓ 6 скриптів |
| Лаб. 5-3 | 3D audio + AudioListener | ✓ 3 PCM-кліпи, просторове аудіо |
| **Лаб. 5-4** | **Final integration** | ✓ HudHint + фінальна WebGL 6.51 МБ |

## 7. Запуск збірки

```bash
cd "/Users/max/KSU/labs/Virtual and augmented reality technologies/PhysicsAR/Build/WebGL"
python3 -m http.server 8000
# відкрити http://localhost:8000/
```

## 8. Висновок

Виконано **повну інтеграцію** проєкту PhysicsAR з трьох сцен візуалізації коливальних систем. Усі компоненти Unity-екосистеми задіяні узгоджено: фізика (Rigidbody, 3 типи Colliders, Trigger, CharacterController, HingeJoint, SpringJoint), графіка (URP PBR-матеріали з процедурними текстурами, частинки, TrailRenderer), анімація (AnimationClip + AnimatorController), аудіо (procedural WAV генерація, 2D-музика + 3D-ефекти), користувацький інтерфейс (OnGUI HUD), архітектура (3 префаби з повторним використанням у різних сценах), програмний код (6 C#-скриптів, що покривають input, scene management, physics events, audio control).

Фінальна WebGL-збірка займає **6.51 МБ** після gzip-компресії, готова до публікації на будь-якому статичному HTTP-сервері. Проєкт повністю реалізує вимоги дисципліни "Технології віртуальної та доповненої реальності".