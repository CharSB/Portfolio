using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class InputManager : Singleton<InputManager>
{
    private GameManager gameManager;

    // Start is called before the first frame update
    void Start()
    {
        gameManager = GameManager.Instance;
    }

    // Update is called once per frame
    void Update()
    {
        /* INPUT SYSTEM
         * 
         * left click - place unlocked point -- WORKS --
         * right click on . - lock point -- WORKS --
         * left click on . and drag - start looking for a second point
         *      if 2nd . found create a stick
         * space is run simulation -- WORKS --
         */

        // SPACEBAR
        if (Input.GetKeyDown(KeyCode.Space))
        {
            gameManager.isRunning = !gameManager.isRunning;
        }

        // LEFT MOUSE CLICK
        if (Input.GetMouseButtonDown(0))
        {
            //raycast when click
            var ray = Camera.main.ScreenPointToRay(Input.mousePosition);
            RaycastHit2D hit = Physics2D.Raycast(ray.origin, ray.direction);
            Debug.DrawRay(ray.origin, ray.direction, Color.magenta);

            if (hit)
            {
                var point = hit.collider.gameObject.GetComponent<Point>();
            }
            else
            {
                Vector2 screenPosition = new Vector2(Input.mousePosition.x, Input.mousePosition.y);
                Vector2 worldPosition = Camera.main.ScreenToWorldPoint(screenPosition);
                gameManager.CreatePoint(worldPosition);
            }
        }


        Point p1 = null, p2 = null;
        // LEFT MOUSE HOLD
        if (Input.GetMouseButton(0))
        {
            //raycast
            var ray = Camera.main.ScreenPointToRay(Input.mousePosition);
            RaycastHit2D hit = Physics2D.Raycast(ray.origin, ray.direction);
            Debug.DrawRay(ray.origin, ray.direction, Color.magenta);

            //hit something
            if(hit)
            {
                // nothing prev hit
                if ( p1 == null)
                {
                    p1 = hit.collider.gameObject.GetComponent<Point>();
                    p1.gameObject.GetComponent<SpriteRenderer>().color = Color.grey;
                }
            }
        }

        // LEFT 
        if(Input.GetMouseButtonUp(0))
        {
            if(p1 != null & p2 != null)
            {
                //make stick
            }
        }

        // RIGHT MOUSE
        if (Input.GetMouseButtonDown(1))
        {
            var ray = Camera.main.ScreenPointToRay(Input.mousePosition);
            RaycastHit2D hit = Physics2D.Raycast(ray.origin, ray.direction);
            Debug.DrawRay(ray.origin, ray.direction, Color.magenta);

            if (hit)
            {
                print("I've been SHOTTTTTT!");
                if (hit.collider.CompareTag("Point"))
                {
                    Point p = hit.collider.GetComponent<Point>();
                    p.SwitchLock();
                }

                if (hit.collider.CompareTag("Stick"))
                {
                    Stick s = hit.collider.GetComponent<Stick>();
                    s.Remove();
                }
            }
        }
    }
}
