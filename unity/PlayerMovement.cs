using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using System.IO;


public class PlayerInfo
{
    public string id;
    public string name;
    public static PlayerInfo CreateFromJSON(string jsonString)
    {
        return JsonUtility.FromJson<PlayerInfo>(jsonString);
    }
}
public class ServerResponse
{
    public string command;
    public string msg;

    public int speed;
    public static ServerResponse CreateFromJSON(string jsonString)
    {
        return JsonUtility.FromJson<ServerResponse>(jsonString);
    }
}

public class PlayerMovement : MonoBehaviour
{
    // Start is called before the first frame update
    Rigidbody rb;
    [SerializeField] float movementSpeed = 2f;
    [SerializeField] float jumpForce = 5f;

    [SerializeField] float horizontalInput = 0f;
    [SerializeField] float verticalInput = 0f;

    private bool isStreaming = false;

    private string contentType = "application/json";
    private bool isMoving = false;

    void Start()
    {
        rb = GetComponent<Rigidbody>();
        isStreaming = true;
        StartCoroutine(StreamObject());
        horizontalInput = Input.GetAxis("Horizontal");
        verticalInput = Input.GetAxis("Vertical");
        rb.velocity = new Vector3((horizontalInput + .1f) * movementSpeed, rb.velocity.y, (verticalInput) * movementSpeed);
    }

    // Update is called once per frame
    void Update()
    {
        // horizontalInput = Input.GetAxis("Horizontal");
        // verticalInput = Input.GetAxis("Vertical");

        // rb.velocity = new Vector3(horizontalInput * movementSpeed, rb.velocity.y, verticalInput * movementSpeed);

        if (Input.GetButtonDown("Jump"))
        {
            rb.velocity = new Vector3(rb.velocity.x, jumpForce, rb.velocity.z);
        }
        OnResume();
        if (Input.GetKeyDown(KeyCode.P) && isStreaming)
        {
            Debug.Log("Stream stopped");
            OnDisable();
        }
        else if (Input.GetKeyDown(KeyCode.R) && isStreaming == false)
        {
            Debug.Log("Stream resumed");
            OnResume();
        }

        if (isMoving)
        {
            transform.position += transform.forward * movementSpeed * Time.deltaTime;
        }
        
    }

    IEnumerator StreamObject()
    {
        PlayerInfo myObject = new PlayerInfo();
        myObject.id = "1";
        myObject.name = "Cylinder";
        string jsonStringTrial = JsonUtility.ToJson(myObject);
        string url = "http://localhost:7000/objects";
        var request = new UnityWebRequest(url, "POST");
        byte[] bodyRaw = System.Text.Encoding.UTF8.GetBytes(jsonStringTrial);
        request.uploadHandler = (UploadHandler)new UploadHandlerRaw(bodyRaw);
        request.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
        request.SetRequestHeader("Content-Type", "application/json");
        yield return request.SendWebRequest();
        var text = request.downloadHandler.text;
        ServerResponse responseObj = JsonUtility.FromJson<ServerResponse>(text);
        // horizontalInput = Input.GetAxis("Horizontal");
        // verticalInput = Input.GetAxis("Vertical");
        Debug.Log("responseObj.command: " + responseObj.command);
        if (responseObj.command == "move")
        {
            isMoving = true;
        } 
        else if (responseObj.command == "stop")
        {
            isMoving = false;
        } 
        else if (responseObj.command == "set_speed")
        {
            movementSpeed = responseObj.speed;
            Debug.Log("Speed: " + movementSpeed);
            
        }
        else if (responseObj.command == "turn_left")
        {
            transform.Rotate(0, -90, 0);
        }
        else if (responseObj.command == "turn_right")
        {
            transform.Rotate(0, 90, 0);
        }
    }
    void OnDisable()
    {
        isStreaming = false;
    }

    void OnResume()
    {
        isStreaming = true;
        StartCoroutine(StreamObject());
    }
}
