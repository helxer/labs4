using UnityEngine;

[RequireComponent(typeof(Collider))]
public class PeriodMeasurer : MonoBehaviour
{
    [Header("Audio")]
    public AudioClip tickClip;
    public AudioSource audioSource;

    private float lastCrossTime = -1f;
    private float measuredPeriod;

    void Awake()
    {
        if (audioSource == null) audioSource = GetComponent<AudioSource>();
    }

    void OnTriggerEnter(Collider other)
    {
        if (!other.attachedRigidbody) return;
        float now = Time.time;
        if (lastCrossTime > 0f)
        {
            measuredPeriod = (now - lastCrossTime) * 2f;
            Debug.Log($"[PeriodMeasurer] T = {measuredPeriod:F3} s");
        }
        lastCrossTime = now;
        if (audioSource != null && tickClip != null) audioSource.PlayOneShot(tickClip);
    }

    public float GetMeasuredPeriod() => measuredPeriod;
}
