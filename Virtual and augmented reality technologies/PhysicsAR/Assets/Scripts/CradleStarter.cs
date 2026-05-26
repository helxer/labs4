using UnityEngine;

public class CradleStarter : MonoBehaviour
{
    [Tooltip("Ball to push at start")]
    public Rigidbody firstBall;

    [Tooltip("Impulse vector applied at Start")]
    public Vector3 initialImpulse = new Vector3(0f, 0f, -2.5f);

    [Tooltip("Delay before applying impulse (seconds)")]
    public float delay = 0.5f;

    void Start()
    {
        if (firstBall != null) Invoke(nameof(Kick), delay);
    }

    void Kick()
    {
        firstBall.AddForce(initialImpulse, ForceMode.Impulse);
    }
}
