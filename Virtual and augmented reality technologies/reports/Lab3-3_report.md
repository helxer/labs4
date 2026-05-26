# Лабораторна робота №3-3

**Дисципліна:** Технології віртуальної та доповненої реальності
**Тема:** Створення елементів та ефектів доповненої реальності за допомогою Unity. Фізика 2D/3D об'єктів (продовження)
**Виконав:** студент групи ______ ___________________

---

## 1. Завдання

1. Продовжити створення проєкту у середовищі Unity 3D.
2. Реалізувати додаткові 3D об'єкти головної сцени та покращити її візуальну якість.
3. Підготувати **анімацію** 3D об'єктів.

## 2. Доданий вміст

### 2.1 PBR-матеріали

Створено 4 матеріали в Universal Render Pipeline / Lit для візуального розрізнення об'єктів:

| Матеріал | Шейдер | Колір (RGBA) | Metallic | Smoothness | Застосовано до |
|----------|--------|--------------|----------|------------|----------------|
| `Mat_Bob.mat` | URP/Lit | (0.2, 0.5, 1.0, 1) — синій | 0.5 | 0.6 | Bob, Bob2 |
| `Mat_Anchor.mat` | URP/Lit | (0.9, 0.2, 0.2, 1) — червоний | 0.3 | 0.4 | Anchor, Anchor2, DecorSign |
| `Mat_Floor.mat` | URP/Lit | (0.7, 0.7, 0.7, 1) — сірий | 0 | 0.3 | Floor |
| `Mat_Observer.mat` | URP/Lit | (0.3, 0.8, 0.3, 1) — зелений | 0.2 | 0.5 | Observer |

### 2.2 Анімація DecorSign

Створено декоративний об'єкт `DecorSign` (куб 1.5×0.3×0.3) над сценою (позиція 0, 6, 0). Колайдер видалено — це чисто візуальний елемент.

**Створені асети анімації:**

| Файл | Тип | Параметри |
|------|-----|-----------|
| `Assets/Animations/DecorSign_Spin.anim` | AnimationClip | length = 4 c, frameRate = 30 fps, loop = true |
| `Assets/Animations/DecorSign_Controller.controller` | AnimatorController | один шар, стан `Spin` (default), без переходів |

**Криві ключових кадрів** (на DecorSign_Spin.anim):

| Час | `Transform.localEulerAnglesRaw.y` |
|-----|----------------------------------|
| 0 с | 0° |
| 2 с | 180° |
| 4 с | 360° |

Це створює плавне обертання знака навколо локальної вісі Y зі швидкістю 90°/с.

**Animator на DecorSign:**
- `runtimeAnimatorController` = `DecorSign_Controller.controller`
- `applyRootMotion` = false

## 3. Оновлена ієрархія сцени

```
01_SimplePendulum
├── Main Camera
├── Directional Light
├── Floor                 (Mat_Floor)
├── Observer              (Mat_Observer + CharacterController)
├── DecorSign             (Mat_Anchor + Animator → Spin)        ← Лаб. 3-3
├── PendulumRoot
│   ├── Anchor            (Mat_Anchor)
│   └── Bob               (Mat_Bob + Rigidbody + HingeJoint)
├── PendulumRoot2
│   ├── Anchor2           (Mat_Anchor)
│   └── Bob2              (Mat_Bob + Rigidbody + HingeJoint)
└── PeriodTrigger         (BoxCollider isTrigger)
```

## 4. Покриття вимог Лаб. 3

| Вимога | Реалізовано | Деталі |
|--------|-------------|--------|
| Rigidbodies | ✓ | Bob, Bob2 |
| Colliders | ✓ | SphereCollider × 2, BoxCollider × 3, MeshCollider, CharacterController |
| Triggers | ✓ | PeriodTrigger (BoxCollider isTrigger) |
| Character Controllers | ✓ | Observer |
| Joints | ✓ | HingeJoint × 2 |
| **Анімація 3D** | ✓ (3-3) | DecorSign_Spin Animator state |
| Ефекти | — | Заплановано у 3-4 |

## 5. Технічні нотатки

1. **Pipeline:** проєкт використовує Universal Render Pipeline (URP). Усі нові матеріали створені з шейдером `Universal Render Pipeline/Lit`, що забезпечує сумісність з WebGL-збіркою (Лаб. 5-1).
2. **Animator vs Animation:** використано модерний Animator (з AnimatorController), а не legacy Animation component — відповідає сучасним практикам Unity 6.
3. **applyRootMotion = false:** анімація обертає лише `localEulerAnglesRaw.y`, не зміщуючи об'єкт у просторі.

## 6. Висновок

У Лаб. 3-3 додано візуальну якість сцени через **PBR-матеріали URP** для усіх об'єктів та реалізовано першу **анімацію** проєкту — обертовий декоративний знак з AnimatorController. На цьому етапі покрито 6 з 7 вимог Лаб. 3 (залишаються лише візуальні ефекти, які реалізуються у Лаб. 3-4). Сцена готова для зйомки скриншотів та подальшого додавання ефектів частинок.