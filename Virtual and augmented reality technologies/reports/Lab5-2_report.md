# Лабораторна робота №5-2

**Дисципліна:** Технології віртуальної та доповненої реальності
**Тема:** Розробка ПЗ за технологією VR/AR. **Скриптовий код управління об'єктами та подіями**
**Виконав:** студент групи 12-441 Рудчук Максим Олегович

---

## 1. Завдання

1. Створити C#-скрипти у проєкті засобами Visual Studio / Unity Editor.
2. Реалізувати **управління 3D-об'єктами** через скрипти.
3. Реалізувати **обробку подій** (Trigger, Input, Scene change).

## 2. Створені скрипти

| Файл | Призначення |
|------|-------------|
| `Assets/Scripts/ObserverController.cs` | WASD-переміщення + RMB-look для CharacterController |
| `Assets/Scripts/SceneRouter.cs` | Перемикання сцен (клавіші 1/2/3/N/R) |
| `Assets/Scripts/PeriodMeasurer.cs` | Вимірювання періоду маятника через Trigger |
| `Assets/Scripts/CradleStarter.cs` | Прикладання імпульсу до першої кульки колиски Ньютона |

Усі скрипти скомпільовані без помилок (verified через `read_console`).

### 2.1 `ObserverController.cs` (керування персонажем)

Працює з компонентом `CharacterController`, доданим у Лаб. 3-2 на об'єкт `Observer`.

```csharp
public float moveSpeed = 4f;
public float gravity = -9.81f;
public float mouseSensitivity = 2f;
public Transform cameraTransform;
```

Логіка:
1. **Input.GetAxis("Horizontal"/"Vertical")** → побудова вектора `move` у локальних осях персонажа.
2. **Гравітація:** velocity.y копиться з `gravity * Time.deltaTime`, при `isGrounded` скидається.
3. **Mouse look** (тільки при затиснутому RMB): yaw обертає всього персонажа навколо Y, pitch обмежений [−80°, 80°] для камери.
4. `controller.Move((move + verticalVelocity) * Time.deltaTime)` — використовує власну колізію CharacterController.

### 2.2 `SceneRouter.cs` (управління сценами)

```csharp
public string[] scenes = { "01_SimplePendulum", "02_SpringPendulum", "03_NewtonsCradle" };
```

**Гарячі клавіші:**
| Клавіша | Дія |
|---------|-----|
| `1` | Завантажити 01_SimplePendulum |
| `2` | Завантажити 02_SpringPendulum |
| `3` | Завантажити 03_NewtonsCradle |
| `N` | Наступна сцена (циклічно) |
| `R` | Перезавантажити поточну сцену (демонстрація reset стану фізики) |

Використовує `UnityEngine.SceneManagement.SceneManager.LoadScene(...)`.

### 2.3 `PeriodMeasurer.cs` (вимірювання періоду через Trigger)

Прив'язаний до `PeriodTrigger` зони у 01_SimplePendulum. Алгоритм:

```csharp
void OnTriggerEnter(Collider other) {
    if (!other.attachedRigidbody) return;
    float now = Time.time;
    if (lastCrossTime > 0f) {
        // Two crossings per full period
        measuredPeriod = (now - lastCrossTime) * 2f;
        Debug.Log($"Measured period: {measuredPeriod:F3} s");
    }
    lastCrossTime = now;
}
```

При кожному перетині маятником зони рівноваги ділиться різниця часів на 0.5 (бо 1 перетин = пів-період). Виміряний період порівнюється з теоретичним T = 2π√(L/g) ≈ 2.84 с для L=2 м.

### 2.4 `CradleStarter.cs` (запуск Newton's Cradle)

Розв'язує проблему "колиска не починає рухатись сама": при Start() через `Invoke(Kick, delay)` прикладає імпульс до першої кульки:

```csharp
public Rigidbody firstBall;
public Vector3 initialImpulse = new Vector3(0, 0, -2.5f);
public float delay = 0.5f;
void Kick() => firstBall.AddForce(initialImpulse, ForceMode.Impulse);
```

Імпульс по осі −Z штовхає кульку 1 у напрямку інших — починається ланцюгова реакція передачі імпульсу.

## 3. Прив'язка скриптів до сцен

### Сцена 01_SimplePendulum

| GameObject | Компонент | Параметри |
|------------|-----------|-----------|
| Main Camera | SceneRouter | default scenes[] |
| Observer | ObserverController | moveSpeed=4, mouseSensitivity=2 |
| PeriodTrigger | PeriodMeasurer | default |

### Сцена 02_SpringPendulum

| GameObject | Компонент |
|------------|-----------|
| Main Camera | SceneRouter |

### Сцена 03_NewtonsCradle

| GameObject | Компонент | Параметри |
|------------|-----------|-----------|
| Main Camera | SceneRouter | — |
| **CradleStarter** (новий) | CradleStarter | firstBall → `CradleRoot/CradleBall_1/Ball.Rigidbody`<br>initialImpulse = (0, 0, −2.5)<br>delay = 0.5 |

## 4. Демонстрація подієвої моделі Unity

Скрипти ілюструють основні Unity event hooks:

| Подія Unity | Де використано |
|-------------|----------------|
| `Awake()` | ObserverController — кешування `CharacterController`, fallback на `Camera.main` |
| `Start()` | CradleStarter — запуск Invoke з затримкою |
| `Update()` | ObserverController, SceneRouter — щокадрова обробка Input |
| `OnTriggerEnter(Collider)` | PeriodMeasurer — обробка фізичної події перетину тригера |
| `Invoke(method, delay)` | CradleStarter — відкладений виклик |

## 5. Покриття вимог Лаб. 5-2

| Вимога | Реалізовано |
|--------|-------------|
| Створення скриптів C# | ✓ 4 скрипти |
| Управління 3D-об'єктами | ✓ ObserverController (CharacterController), CradleStarter (Rigidbody.AddForce) |
| Управління подіями | ✓ OnTriggerEnter, Input.GetKeyDown, SceneManager |

## 6. Висновок

У ході виконання Лаб. 5-2 створено 4 C#-скрипти, що забезпечують повне керування проєктом: `ObserverController` для переміщення спостерігача, `SceneRouter` для навігації між трьома сценами проєкту, `PeriodMeasurer` для вимірювання періоду маятника через Trigger-події, та `CradleStarter` для автоматичного запуску колиски Ньютона. Усі скрипти прив'язані до відповідних GameObjects через MCP API (`manage_components`), що демонструє програмний підхід до конфігурації Unity-сцен. Проєкт тепер інтерактивний і готовий до додавання звукового супроводу у Лаб. 5-3.