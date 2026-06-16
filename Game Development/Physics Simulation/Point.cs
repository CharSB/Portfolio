using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Random = UnityEngine.Random;

[Serializable]
public class Point : MonoBehaviour
{
    [SerializeField] private float offset_x;
    [SerializeField] private float offset_y;
    public Vector2 Pos, oldPos;
    public bool locked = true;

    GameManager gameManager;
    LagueInput lagueInput;
    SpriteRenderer srenderer;

    private void Awake()
    {
        Pos.x = gameObject.transform.position.x;
        Pos.y = gameObject.transform.position.y;

        if(oldPos == Vector2.zero)
        {
            oldPos.x = Random.Range(-.5f, .6f);
            oldPos.y = Random.Range(-.5f, .6f);
        }

        oldPos.x = Pos.x + offset_x;
        oldPos.y = Pos.y + offset_y;
    }
    // Start is called before the first frame update
    void Start()
    {
        gameManager = GameManager.Instance;
        lagueInput = LagueInput.Instance;
        if (!gameManager.points.Contains(this))
            gameManager.points.Add(this);

        srenderer = gameObject.GetComponent<SpriteRenderer>();
        srenderer.color = locked ? Color.red : Color.white;
    }

    public void SwitchLock()
    {
        locked = locked ? false : true ;
        srenderer.color = locked ? Color.red : Color.white;
    }

    public void updatePosition()
    {
        gameObject.transform.position = Pos;
    }

    public void Remove()
    {
        gameManager.points.Remove(this);
        foreach(Stick stick in gameManager.sticks)
        {
            stick.CheckPoints();
        }
        lagueInput.CheckTemps(this);
        Destroy(gameObject);
    }
}
