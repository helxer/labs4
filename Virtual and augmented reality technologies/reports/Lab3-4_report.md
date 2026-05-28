# Лабораторна робота №3-4

**Дисципліна:** Технології віртуальної та доповненої реальності
**Тема:** Створення елементів та ефектів доповненої реальності за допомогою Unity. Фізика 2D/3D об'єктів (продовження)
**Виконав:** студент групи 12-441 Рудчук Максим Олегович

---

## 1. Завдання

1. Продовжити створення проєкту у середовищі Unity 3D.
2. **Створити та додати 2D або 3D ефекти** до сцени AR.
3. Завершити покриття усіх вимог Лаб. 3 (фізика, анімація, ефекти).

## 2. Додані ефекти

### 2.1 TrailRenderer — слід руху маятника

На обидва маятникові тіла (Bob, Bob2) додано компонент `TrailRenderer`, що візуалізує траєкторію руху у вигляді світлого сліду. Слід згасає за заданий час.

| Параметр | Bob | Bob2 |
|----------|-----|------|
| `time` (тривалість сліду) | 1.5 с | 1.2 с |
| `startWidth` | 0.10 | 0.08 |
| `endWidth` | 0 | 0 |
| `minVertexDistance` | 0.05 | 0.05 |
| `emitting` | true | true |
| `sharedMaterial` | `Mat_Trail` | `Mat_Trail` |

Створено матеріал `Assets/Materials/Mat_Trail.mat`:
- Шейдер `Universal Render Pipeline/Unlit`
- Колір (0.5, 0.85, 1.0, 0.7) — світло-блакитний, напівпрозорий

### 2.2 ParticleSystem — іскри у точці пивоту

GameObject `Sparkle` з компонентом `ParticleSystem` розміщений у точці пивоту першого маятника (0, 4, 0). При запуску сцени з пивоту випромінюються частинки, що додає візуальної динаміки.

GameObject також містить автоматично доданий `ParticleSystemRenderer` для рендеру частинок.

## 3. Фінальна ієрархія сцени

```
01_SimplePendulum
├── Main Camera
├── Directional Light
├── Floor                 (Mat_Floor)
├── Observer              (Mat_Observer + CharacterController)
├── DecorSign             (Mat_Anchor + Animator → Spin)
├── Sparkle               (ParticleSystem)                      ← Лаб. 3-4
├── PendulumRoot
│   ├── Anchor            (Mat_Anchor)
│   └── Bob               (Mat_Bob + Rigidbody + HingeJoint + TrailRenderer) ← Trail у 3-4
├── PendulumRoot2
│   ├── Anchor2           (Mat_Anchor)
│   └── Bob2              (Mat_Bob + Rigidbody + HingeJoint + TrailRenderer) ← Trail у 3-4
└── PeriodTrigger         (BoxCollider isTrigger)
```

## 4. Повне покриття вимог Лаб. 3

| Вимога | Об'єкт | Sub-lab |
|--------|--------|---------|
| Rigidbodies | Bob, Bob2 | 3-1 |
| Colliders (Sphere/Box/Mesh) | Bob, Bob2, Anchor, Anchor2, Floor | 3-1 |
| Triggers | PeriodTrigger | 3-1 |
| Character Controllers | Observer | 3-2 |
| Joints (HingeJoint) | Bob, Bob2 | 3-1, 3-2 |
| Анімація 3D | DecorSign | 3-3 |
| **Ефекти 3D** | TrailRenderer на Bob/Bob2 + ParticleSystem (Sparkle) | **3-4** |

## 5. Технічні нотатки

1. **TrailRenderer** як вибір для сліду маятника замість Line Renderer — він автоматично оновлюється на основі позиції GameObject протягом часу, що ідеально для динамічного руху без додаткового скриптування.
2. **URP/Unlit** для матеріалу сліду — гарантує яскравий, постійний колір незалежно від освітлення.
3. **Розташування Sparkle** у точці пивоту створює природне зорове акцентування центру системи.

## 6. Висновок

Лаб. 3 повністю завершено. У сцені `01_SimplePendulum.unity` реалізовано:
- усі **5 типів фізичних компонентів** (Rigidbody, Collider, Trigger, CharacterController, Joint);
- **анімацію** (Animator + AnimationClip);
- **3D ефекти** (TrailRenderer × 2 + ParticleSystem).

Сцена готова для розширення у Лаб. 4 (декоратор сцен, префаби, ассети) та Лаб. 5 (WebGL build, скрипти, аудіо).