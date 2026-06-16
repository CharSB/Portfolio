using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Stick : MonoBehaviour
{
    GameManager gameManager;

    public Point pointA, pointB;
    [SerializeField] private Point[] _points;
    public Point[] Points
    {
        get { return _points; }
    }

    public float length;

    private LineRenderer lineRenderer;
    private EdgeCollider2D edgeCollider;

    private void Awake()
    {
        lineRenderer = GetComponent<LineRenderer>();
        edgeCollider = GetComponent<EdgeCollider2D>();
        _points = new Point[2];
    }

    private void Start()
    {
        gameManager = GameManager.Instance;
        if (!gameManager.sticks.Contains(this))
            gameManager.sticks.Add(this);

        if(length == 0)
        {
            length = Vector2.Distance(pointA.Pos, pointB.Pos);
        }

        _points[0] = pointA;
        _points[1] = pointB;
    }

    public void SetupLine(Point[] points)
    {
        lineRenderer.positionCount = points.Length;
        //_points = points;
    }

    // Update is called once per frame
    void Update()
    {
        for(int i = 0; i < 2; i++)
        {
            lineRenderer.SetPosition(i, _points[i].Pos);
        }
        edgeCollider.points = new Vector2[]{ pointA.Pos, pointB.Pos};
    }

    public void CheckPoints()
    {
        if (pointA == null)
            Remove();
        if (pointB == null)
            Remove();

    }

    public void Remove()
    {
        gameManager.sticks.Remove(this);
        Destroy(gameObject);
    }
}
