using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GameManager : Singleton<GameManager>
{
    [Header("Walls")]
    [SerializeField] float height, width;
    [Space]

    [Header("Simulation vars")]
    [SerializeField] float gravity;
    [SerializeField] float friction;
    [SerializeField] float bounce;
    [SerializeField] int iterations;
    [Space]

    [Header("Prefabs")]
    public GameObject pointPrefab;
    public GameObject stickPrefeb;
    public LayerMask PointMask;
    [Space]

    // start a list of points
    [SerializeField]
    public List<Point> points = new List<Point>();
    // start a list of points
    [SerializeField]
    public List<Stick> sticks = new List<Stick>();

    public GameObject lastPoint;
    public bool isRunning = false;
    

    // Start is called before the first frame update
    void Start()
    {
        if(height == 0f || width ==0f)
        {
            height = Camera.main.orthographicSize;
            width = height * (Screen.width / Screen.height);
        }
    }

    // Physics calls to do 
    void FixedUpdate()
    {
        if (points.Count > 0 && isRunning)
        {
            Simulate();
        }
    }

    // Update is called once per frame
    void Update()
    {
        foreach(Stick s in sticks)
        {
            s.SetupLine(s.Points);
        }
    }

    private void Simulate()
    {
        //Points
        foreach(Point p in points)
        {
            if(!p.locked)
            {
                var posPre = p.Pos;
                Vector2 vector = p.Pos - p.oldPos;

                p.Pos += vector * friction;
                p.Pos += Vector2.down * gravity * Time.deltaTime * Time.deltaTime;
                p.oldPos = posPre;

                if (p.Pos.x > width)
                {
                    p.Pos.x = width;
                    p.oldPos.x = p.Pos.x + vector.x * bounce;
                }
                else if(p.Pos.x < -width)
                {
                    p.Pos.x = -width;
                    p.oldPos.x = p.Pos.x + vector.x * bounce;
                }
                if (p.Pos.y > height)
                {
                    p.Pos.y = height;
                    p.oldPos.y = p.Pos.y + vector.y * bounce;
                }
                else if (p.Pos.y < -height)
                {
                    p.Pos.y = -height;
                    p.oldPos.y = p.Pos.y + vector.y * bounce;
                }

                p.updatePosition();
            }
        }

        for (int i = 0; i < iterations; i++)
        {
            foreach (Stick s in sticks)
            {
                Vector2 stickCentre = (s.pointA.Pos + s.pointB.Pos) / 2;
                Vector2 stickDir = (s.pointA.Pos - s.pointB.Pos).normalized;
                if (!s.pointA.locked)
                    s.pointA.Pos = stickCentre + stickDir * s.length / 2;
                if (!s.pointB.locked)
                    s.pointB.Pos = stickCentre - stickDir * s.length / 2;
            }
        }
        
    }


    public GameObject CreatePoint(Vector2 position)
    {
        var point = Instantiate(pointPrefab, position, Quaternion.identity);
        return point;
    }

    public void CreateStick(GameObject p1, GameObject p2)
    {
        var stick = Instantiate(stickPrefeb);
        Stick s = stick.GetComponent<Stick>();
        s.pointA = p1.GetComponent<Point>();
        s.pointB = p2.GetComponent<Point>();
        s.SetupLine(s.Points);
    }

    public RaycastHit2D OverThing()
    {
        var ray = Camera.main.ScreenPointToRay(Input.mousePosition);
        RaycastHit2D hit = Physics2D.Raycast(ray.origin, ray.direction);
        return hit;
    }
    public RaycastHit2D OverThing(LayerMask layerMask)
    {
        var ray = Camera.main.ScreenPointToRay(Input.mousePosition);
        RaycastHit2D hit = Physics2D.Raycast(ray.origin, ray.direction, Mathf.Infinity ,layerMask);
        return hit;
    }
}
