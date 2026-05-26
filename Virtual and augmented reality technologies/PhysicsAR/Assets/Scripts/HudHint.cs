using UnityEngine;

public class HudHint : MonoBehaviour
{
    private GUIStyle style;

    void OnGUI()
    {
        if (style == null)
        {
            style = new GUIStyle(GUI.skin.label);
            style.fontSize = 16;
            style.normal.textColor = new Color(1f, 1f, 1f, 0.85f);
        }
        GUI.Box(new Rect(10, 10, 320, 110), "");
        GUI.Label(new Rect(20, 20, 300, 24), "PhysicsAR — Pendulum Visualizations", style);
        GUI.Label(new Rect(20, 44, 300, 20), "1 / 2 / 3  — switch scene", style);
        GUI.Label(new Rect(20, 64, 300, 20), "N  — next  ·  R  — reset", style);
        GUI.Label(new Rect(20, 84, 300, 20), "RMB + mouse — look  ·  WASD — move", style);
    }
}
