# Лабораторна робота №4-4

**Дисципліна:** Технології віртуальної та доповненої реальності
**Тема:** Розроблення декоратору сцен з використанням префабів. **Робота з матеріалами та текстурами**
**Виконав:** студент групи ______ ___________________

---

## 1. Завдання

1. Створити **процедурні текстури** для проєкту.
2. Реалізувати нові PBR-матеріали з варіацією металевості, гладкості, текстурування.
3. Застосувати нові матеріали до префабів — оцінити перевагу централізованого редагування.

## 2. Процедурно згенеровані текстури

Замість використання зовнішніх ассетів, текстури **програмно згенеровано** через `Texture2D` API. Це підкреслює можливості Unity Editor для процедурної генерації.

### 2.1 `Assets/Textures/Checker.png` (256×256)

8×8 шахова сітка для підлоги. Світлі клітини — RGB (0.85, 0.85, 0.88); темні — RGB (0.35, 0.35, 0.40). Імпортовано з налаштуваннями: `wrapMode=Repeat`, `filterMode=Bilinear`.

### 2.2 `Assets/Textures/Wood.png` (256×256)

Текстура деревини на основі **Perlin Noise + синусоїдального патерну**. Базовий колір (0.55, 0.32, 0.16) — теплий коричневий; темна смуга (0.32, 0.18, 0.08). Імпорт з `wrapMode=Repeat`.

Код генерації:
```csharp
float n = Mathf.PerlinNoise(x * 0.02f, y * 0.005f);
float grain = Mathf.Sin(y * 0.15f + n * 4f) * 0.5f + 0.5f;
Color c = Color.Lerp(baseC, darkC, grain * 0.5f + n * 0.3f);
```

## 3. Нові PBR-матеріали

| Файл | Шейдер | Колір базовий | Metallic | Smoothness | Texture |
|------|--------|---------------|----------|------------|---------|
| `Mat_FloorChecker.mat` | URP/Lit | білий | 0 | 0.4 | Checker.png, tiling 4×4 |
| `Mat_Wood.mat` | URP/Lit | білий | 0 | 0.2 | Wood.png, tiling 1×3 |
| `Mat_Steel.mat` | URP/Lit | (0.78, 0.82, 0.86) | **1.0** | **0.85** | — |
| `Mat_Brass.mat` | URP/Lit | (0.85, 0.65, 0.25) | **0.95** | 0.7 | — |

Контрастна варіація metallic/smoothness демонструє різницю між:
- **Неметалічними** поверхнями (Wood, FloorChecker — лише дифузне відбиття)
- **Металевими** (Steel — дзеркальне; Brass — золотисте, трохи менше гладкість)

## 4. Застосування матеріалів через префаби

### 4.1 `DecorColumn.prefab` → `Mat_Wood`

Через `manage_prefabs(modify_contents)` змінено `MeshRenderer.m_Materials[0]` на `Mat_Wood.mat`. Зміна **автоматично поширилась на всі 6 інстансів** колон у двох сценах:
- 4 інстанси у `02_SpringPendulum.unity`
- 2 інстанси (FrameSupport_L, FrameSupport_R) у `03_NewtonsCradle.unity`

### 4.2 `CradleBall.prefab` → `Mat_Steel`

Використано **Prefab Stage workflow**:
1. `open_prefab_stage("Assets/Prefabs/CradleBall.prefab")` — відкрив префаб у режимі редагування.
2. `manage_components(set_property)` на `Ball` MeshRenderer → `Mat_Steel.mat`.
3. `save_prefab_stage` + `close_prefab_stage` — зберегли зміну.

**Результат:** усі 5 інстансів CradleBall у сцені `03_NewtonsCradle` отримали сталевий вигляд за 3 виклики API.

### 4.3 Заміна матеріалів у сценах

| Об'єкт | Сцена | Новий матеріал |
|--------|-------|----------------|
| `Floor` | 01_SimplePendulum | Mat_FloorChecker |
| `Floor` | 02_SpringPendulum | Mat_FloorChecker |
| `Floor` | 03_NewtonsCradle | Mat_FloorChecker |
| `CrossBeam` | 03_NewtonsCradle | Mat_Brass |

## 5. Повний інвентар ассетів проєкту

### `Assets/Prefabs/`
- `DecorColumn.prefab` (Mat_Wood)
- `SpringPendulum.prefab`
- `CradleBall.prefab` (Mat_Steel)

### `Assets/Materials/`
- Mat_Bob, Mat_Anchor, Mat_Floor (legacy), Mat_Observer, Mat_Trail
- **Mat_FloorChecker, Mat_Wood, Mat_Steel, Mat_Brass** (нові у 4-4)

### `Assets/Textures/`
- **Checker.png, Wood.png** (процедурні)

### `Assets/Animations/`
- DecorSign_Spin.anim, DecorSign_Controller.controller

### `Assets/Scenes/`
- 01_SimplePendulum.unity (з Лаб. 3)
- 02_SpringPendulum.unity (з Лаб. 4-1)
- 03_NewtonsCradle.unity (з Лаб. 4-3)

## 6. Демонстрація переваги префабів

Без префабів зміна матеріалу 6 колон потребувала би 6 окремих операцій + ручного відстеження інстансів у двох сценах. З префабом — **одна операція** на ассеті префабу автоматично оновлює всі його інстанси у всіх сценах. Це підтверджує архітектурну цінність префаб-підходу для масштабованих AR-проєктів.

## 7. Висновок

У ході виконання Лаб. 4-4 створено **процедурні текстури** (Checker, Wood) безпосередньо у Unity Editor через `Texture2D` API без зовнішніх інструментів. Створено 4 нових PBR-матеріали з контрастними фізичними параметрами (металеві Steel/Brass vs діелектричні Wood/FloorChecker). Матеріали застосовано через префаби — централізована модифікація автоматично поширилась на 11+ інстансів у трьох сценах проєкту. Лабораторна робота 4 повністю завершена; проєкт готовий до фінального етапу — Лаб. 5 (WebGL-публікація, скрипти C#, аудіо).