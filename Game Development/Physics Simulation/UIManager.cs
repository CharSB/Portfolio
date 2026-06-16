using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class UIManager : Singleton<UIManager>
{
    [SerializeField] public Toggle delete;
    public Toggle astick;

    public void Delete(bool changeTo)
    {
        delete.isOn = changeTo;
    }

    public void Astick(bool changeTo)
    {
        astick.isOn = changeTo;
    }
}
