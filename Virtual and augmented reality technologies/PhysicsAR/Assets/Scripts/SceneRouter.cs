using UnityEngine;
using UnityEngine.SceneManagement;

public class SceneRouter : MonoBehaviour
{
    [Tooltip("Scene names in Build Settings (must be added there)")]
    public string[] scenes = { "01_SimplePendulum", "02_SpringPendulum", "03_NewtonsCradle" };

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Alpha1)) LoadByIndex(0);
        if (Input.GetKeyDown(KeyCode.Alpha2)) LoadByIndex(1);
        if (Input.GetKeyDown(KeyCode.Alpha3)) LoadByIndex(2);
        if (Input.GetKeyDown(KeyCode.R)) SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex);
        if (Input.GetKeyDown(KeyCode.N)) LoadByIndex((SceneManager.GetActiveScene().buildIndex + 1) % scenes.Length);
    }

    public void LoadByIndex(int i)
    {
        if (i >= 0 && i < scenes.Length) SceneManager.LoadScene(scenes[i]);
    }
}
