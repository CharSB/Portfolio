using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public abstract class Singleton<T> : MonoBehaviour where T : Singleton<T>
{
    private static T _instance;
    public static T Instance
    {
        get
        {
            if(_instance == null)
            {
                Debug.Log(typeof(T).ToString() + ": new GameObject instanciated");
                GameObject gameObject = new GameObject(typeof(T).ToString());
                gameObject.AddComponent<T>();
            }
            return _instance;
        }
    }

    public void Awake()
    {
        _instance = (T)this;
    }
}
