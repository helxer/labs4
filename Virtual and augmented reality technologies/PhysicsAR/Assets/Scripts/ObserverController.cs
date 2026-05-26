using UnityEngine;

public class ObserverController : MonoBehaviour
{
    [Header("Movement")]
    public float moveSpeed = 4f;
    public float gravity = -9.81f;

    [Header("Mouse Look")]
    public float mouseSensitivity = 2f;
    public Transform cameraTransform;

    private CharacterController controller;
    private Vector3 velocity;
    private float pitch;

    void Awake()
    {
        controller = GetComponent<CharacterController>();
        if (cameraTransform == null && Camera.main != null)
            cameraTransform = Camera.main.transform;
    }

    void Update()
    {
        float h = Input.GetAxis("Horizontal");
        float v = Input.GetAxis("Vertical");
        Vector3 move = (transform.right * h + transform.forward * v) * moveSpeed;

        if (controller.isGrounded && velocity.y < 0f) velocity.y = -2f;
        velocity.y += gravity * Time.deltaTime;

        controller.Move((move + new Vector3(0f, velocity.y, 0f)) * Time.deltaTime);

        if (Input.GetMouseButton(1) && cameraTransform != null)
        {
            float yaw = Input.GetAxis("Mouse X") * mouseSensitivity;
            float pitchDelta = -Input.GetAxis("Mouse Y") * mouseSensitivity;
            transform.Rotate(0f, yaw, 0f, Space.World);
            pitch = Mathf.Clamp(pitch + pitchDelta, -80f, 80f);
            cameraTransform.localEulerAngles = new Vector3(pitch, cameraTransform.localEulerAngles.y, 0f);
        }
    }
}
