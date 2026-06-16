using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LagueInput : Singleton<LagueInput>
{
    // STATES
    public bool DELETE = false;
    public bool AUTOSTICK = false;
    public bool isDrawing = false;

    // TEMPS
    private RaycastHit2D prevHit;
    [SerializeField] private GameObject lastPoint;
    [SerializeField] private GameObject curPoint;

    private GameManager gameManager;
    private UIManager UIManager;

    // Start is called before the first frame update
    void Start()
    {
        gameManager = GameManager.Instance;
        UIManager = UIManager.Instance;

        curPoint = gameManager.points[gameManager.points.Count-1].gameObject;
        lastPoint = gameManager.points[gameManager.points.Count - 2].gameObject;
        if (lastPoint != null)
            print("last point found");
    }

    // Update is called once per frame
    void Update()
    {
        // SPACEBAR
        if (Input.GetKeyDown(KeyCode.Space))
        {
            gameManager.isRunning = !gameManager.isRunning;
        }

        // D 
        if (Input.GetKeyDown(KeyCode.D))
        {
            DELETE = !DELETE;
            print("DELETE is now: " + DELETE);
            UIManager.Delete(DELETE);
        }

        // A 
        if (Input.GetKeyDown(KeyCode.A))
        {
            AUTOSTICK = !AUTOSTICK;
            print("AUTOSTICK is now: " + AUTOSTICK);
            UIManager.Astick(AUTOSTICK);
        }

        #region REGULAR
        if (!DELETE)
        { 
            // LEFT DOWN
            if (Input.GetMouseButtonDown(0))
            {
                if (gameManager.OverThing(gameManager.PointMask))
                {
                    print("starting to draw line");
                    isDrawing = true;
                    lastPoint = curPoint;
                    curPoint = gameManager.OverThing(gameManager.PointMask).collider.gameObject;
                }
                else
                {
                    print("Create Point");
                    Vector2 screenPosition = new Vector2(Input.mousePosition.x, Input.mousePosition.y);
                    Vector2 worldPosition = Camera.main.ScreenToWorldPoint(screenPosition);
                    var p = gameManager.CreatePoint(worldPosition);

                    lastPoint = curPoint;
                    curPoint = p;

                    if (AUTOSTICK)
                    {
                        gameManager.CreateStick(curPoint, lastPoint);
                    }
                }
            }

            // LEFT UP
            if (Input.GetMouseButtonUp(0))
            {
                if (gameManager.OverThing(gameManager.PointMask) && isDrawing)
                {
                    print("Create Stick");
                    lastPoint = curPoint;
                    curPoint = gameManager.OverThing(gameManager.PointMask).collider.gameObject;
                    gameManager.CreateStick(curPoint, lastPoint);
                }

                isDrawing = false;
                print("Stopped Drawing");
            }

            // RIGHT DOWN
            if (Input.GetMouseButtonDown(1))
            {
                if (gameManager.OverThing())
                {
                    print("Lock Point");
                    if (gameManager.OverThing(gameManager.PointMask).collider.CompareTag("Point"))
                    {
                        Point p = gameManager.OverThing(gameManager.PointMask).collider.GetComponent<Point>();
                        p.SwitchLock();
                    }
                }
            }
        }
        #endregion

        // WORKS PERFECTLY
        #region DELETE
        if (DELETE)
        {
            // LEFT DOWN
            if (Input.GetMouseButton(0))
            {
                if (gameManager.OverThing())
                {
                    if(gameManager.OverThing().collider.GetComponent<Point>())
                    {
                        var p = gameManager.OverThing().collider.GetComponent<Point>();
                        p.Remove();
                    }
                    else if (gameManager.OverThing().collider.GetComponent<Stick>())
                    {
                        var s = gameManager.OverThing().collider.GetComponent<Stick>();
                        s.Remove();
                    }
                }
            }
        }
        #endregion

    }

    public void CheckTemps(Point point)
    {
        if (point.gameObject == lastPoint)
            lastPoint = null;
        if (point.gameObject == curPoint)
            curPoint = null;
    }
}
