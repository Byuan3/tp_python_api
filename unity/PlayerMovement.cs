using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using System.IO;


public class MyClass
{
    public string id;
    public string name;
}

public class PlayerMovement : MonoBehaviour
{
    // Start is called before the first frame update
    Rigidbody rb;
    [SerializeField] float movementSpeed = 6f;
    [SerializeField] float jumpForce = 5f;

    private bool isStreaming = false;

    private string contentType = "application/json";

    void Start()
    {
        rb = GetComponent<Rigidbody>();
        isStreaming = true;
        StartCoroutine(StreamObject());



    }

    // Update is called once per frame
    void Update()
    {
        float horizontalInput = Input.GetAxis("Horizontal");
        float verticalInput = Input.GetAxis("Vertical");

        rb.velocity = new Vector3(horizontalInput * movementSpeed, rb.velocity.y, verticalInput * movementSpeed);

        if (Input.GetButtonDown("Jump"))
        {
            rb.velocity = new Vector3(rb.velocity.x, jumpForce, rb.velocity.z);
        }
        // OnResume();
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


    }

    IEnumerator StreamObject()
    {
        MyClass myObject = new MyClass();
        myObject.id = "1";
        myObject.name = "Cylinder";
        string jsonStringTrial = JsonUtility.ToJson(myObject);
        string url = "http://localhost:7000/objects";
        // string bodyJsonString ='{"id":"cylinder",}';
        var request = new UnityWebRequest(url, "POST");
        byte[] bodyRaw = System.Text.Encoding.UTF8.GetBytes(jsonStringTrial);
        request.uploadHandler = (UploadHandler)new UploadHandlerRaw(bodyRaw);
        request.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
        request.SetRequestHeader("Content-Type", "application/json");
        yield return request.SendWebRequest();
        Debug.Log("Status Code: " + request.downloadHandler.text);
    }

    // IEnumerator StreamObject()
    // {

    //     // var request = new UnityWebRequest("http://localhost:7000/objects", "POST");
    //     // string bodyJsonString = @"{
    //     //         'id':'cylinder', 
    //     //     }";
    //     // byte[] bodyRaw = System.Text.Encoding.UTF8.GetBytes(bodyJsonString);
    //     // request.uploadHandler = (UploadHandler)new UploadHandlerRaw(bodyRaw);
    //     // request.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
    //     // request.SetRequestHeader("Content-Type", "application/json");
    //     // yield return request.SendWebRequest();
    //     // Debug.Log("Status Code: " + request.responseCode);

    //     while (isStreaming)
    //     {

    //         string bodyJsonString = @"{
    //             'id':'cylinder', 
    //         }";
    //         byte[] bodyRaw = System.Text.Encoding.UTF8.GetBytes(bodyJsonString);
    //         yield return new WaitForEndOfFrame();
    //         ;

    //         WWWForm form = new WWWForm();
    //         float horizontalInput = Input.GetAxis("Horizontal");
    //         float verticalInput = Input.GetAxis("Vertical");
    //         form.AddField("Content-Type", contentType);
    //         form.AddField("Content-Length", bodyJsonString.Length.ToString());
    //         // byte[] postData = System.Text.Encoding.UTF8.GetBytes(json);
    //         form.AddBinaryData("json", bodyRaw);
    //         UnityWebRequest www = UnityWebRequest.Post("http://localhost:7000/objects", form);
    //         www.SetRequestHeader("Content-Type", "application/json");
    //         using (www)
    //         {

    //             yield return www.SendWebRequest();

    //             if (www.result != UnityWebRequest.Result.Success)
    //             {
    //                 Debug.Log(www.error);
    //             }
    //             else
    //             {
    //                 Debug.Log("Server Response: " + www.downloadHandler.text);
    //             }

    //             yield return null;
    //         }
    //     }
    // }

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
