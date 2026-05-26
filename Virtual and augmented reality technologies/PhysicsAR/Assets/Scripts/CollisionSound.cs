using UnityEngine;

[RequireComponent(typeof(AudioSource))]
public class CollisionSound : MonoBehaviour
{
    public AudioClip clip;
    [Range(0f, 1f)] public float minImpulse = 0.3f;
    [Range(0f, 2f)] public float volumeScale = 1f;

    private AudioSource src;

    void Awake() { src = GetComponent<AudioSource>(); }

    void OnCollisionEnter(Collision c)
    {
        if (clip == null) return;
        float impulse = c.impulse.magnitude;
        if (impulse < minImpulse) return;
        src.PlayOneShot(clip, Mathf.Clamp01(impulse * 0.1f) * volumeScale);
    }
}
