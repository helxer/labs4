# Лабораторна робота №4-2

**Дисципліна:** Технології віртуальної та доповненої реальності
**Тема:** Розроблення декоратору сцен. Створення об'єктів **префаби (prefabs)** та ассети (assets)
**Виконав:** студент групи 12-441 Рудчук Максим Олегович

---

## 1. Завдання

1. Створити об'єкти **prefabs** з повторюваних елементів сцени.
2. Використати створені префаби для заповнення сцени `02_SpringPendulum.unity`.
3. Продемонструвати поширення змін префабу на усі його інстанси.

## 2. Створені префаби

### 2.1 `Assets/Prefabs/DecorColumn.prefab`

Префаб однієї колони, який замінив 4 ідентичні циліндри декоратору сцен:

| Компонент | Параметри |
|-----------|-----------|
| Transform | scale (0.5, 1.5, 0.5) |
| MeshFilter | Cylinder primitive |
| CapsuleCollider | автоматичний |
| MeshRenderer | sharedMaterial = `Mat_Anchor.mat` (червоний) |

**Хід створення:**
1. У сцені вже існував `Column_NW` (з Лаб. 4-1).
2. Виконано `manage_prefabs(create_from_gameobject)` → створено `Assets/Prefabs/DecorColumn.prefab`. Оригінальний GameObject став інстансом префабу.
3. Видалено інші 3 копії (`Column_NE`, `_SW`, `_SE`) — звичайні дублікати.
4. Створено 3 нових інстанси префабу через `manage_gameobject(create, prefab_path=…)`:
   - `DecorColumn_NE` at (4, 1.5, 4)
   - `DecorColumn_SW` at (–4, 1.5, –4)
   - `DecorColumn_SE` at (4, 1.5, –4)
5. Модифіковано сам префаб через `manage_prefabs(modify_contents)` — призначено матеріал `Mat_Anchor` (`m_Materials[0]`). Зміна автоматично поширилась на усі 4 інстанси у сцені.

### 2.2 `Assets/Prefabs/SpringPendulum.prefab`

Самодостатній префаб пружинного маятника як єдине ціле:

```
SpringPendulumUnit (root, Transform)
├── SpringAnchor   (Cube + BoxCollider + Rigidbody[kinematic])
└── SpringBob      (Sphere + SphereCollider + Rigidbody + SpringJoint → SpringAnchor)
```

**Хід створення:**
1. Створено новий root GameObject `SpringPendulumUnit` у позиції (0, 0, 0).
2. Через `manage_gameobject(modify, parent="SpringPendulumUnit")` перенесено `SpringAnchor` і `SpringBob` під цей root.
3. `manage_prefabs(create_from_gameobject, prefab_path="Assets/Prefabs/SpringPendulum.prefab")` створив префаб з рутового об'єкта. Внутрішня референція `SpringJoint.connectedBody` зберігається коректно, оскільки обидва об'єкти знаходяться у межах одного префабу.

## 3. Ієрархія сцени після рефакторингу

```
02_SpringPendulum
├── Main Camera
├── Directional Light
├── Floor
├── SpringPendulumUnit               ← інстанс SpringPendulum.prefab
│   ├── SpringAnchor
│   └── SpringBob (SpringJoint → SpringAnchor)
└── Decor_Root
    ├── DecorColumn       ← інстанс DecorColumn.prefab (NW)
    ├── DecorColumn_NE    ← інстанс DecorColumn.prefab
    ├── DecorColumn_SW    ← інстанс DecorColumn.prefab
    ├── DecorColumn_SE    ← інстанс DecorColumn.prefab
    └── BackWall
```

## 4. Переваги префаб-рефакторингу

| Аспект | До (Лаб. 4-1) | Після (Лаб. 4-2) |
|--------|---------------|------------------|
| Кількість унікальних об'єктів-колон | 4 (`Column_NW…SE`) | 1 префаб + 4 інстанси |
| Зміна матеріалу колон | Треба редагувати 4 об'єкти | 1 правка в префабі → 4 оновлення |
| Перевикористання у нових сценах | Копіювати-вставити | Інстансіювати префаб |
| Збереження SpringJoint при дублюванні | Ризик розриву референції | Гарантовано (внутрішня референція префабу) |

## 5. Покриття вимог Лаб. 4 на цей момент

| Вимога | Реалізовано | Деталі |
|--------|-------------|--------|
| Створення додаткових сцен | ✓ (4-1) | `02_SpringPendulum.unity` |
| Декоратор сцен | ✓ (4-1) | `Decor_Root` |
| Rigidbody / Collider / Trigger / Joint | ✓ | SpringJoint, Rigidbody, Colliders |
| Анімація | ✓ (з Лаб. 3) | DecorSign_Spin |
| Ефекти 2D/3D | ✓ (з Лаб. 3) | TrailRenderer, ParticleSystem |
| **Префаби (prefabs)** | ✓ (4-2) | DecorColumn, SpringPendulum |
| Ассети (матеріали) | ✓ | Mat_Bob/Anchor/Floor/Observer/Trail |
| Текстури PBR | Не реалізовано | Заплановано у 4-4 |

## 6. Висновок

У ході виконання Лаб. 4-2 виконано **префаб-рефакторинг** сцени `02_SpringPendulum.unity`. Створено два префаби: `DecorColumn.prefab` (повторюваний декоративний елемент) та `SpringPendulum.prefab` (самодостатня фізична одиниця з SpringJoint). Префаби дозволили скоротити кількість унікальних об'єктів-копій у сцені та забезпечили можливість централізованого редагування — зміна матеріалу одного префабу автоматично поширилась на 4 інстанси у сцені. Ця архітектура буде використана у Лаб. 4-3 для побудови сцени маятника Ньютона з 5 однакових кульок.