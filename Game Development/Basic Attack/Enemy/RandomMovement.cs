using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class RandomMovement : MonoBehaviour
{
    /* SUMMARY
     * The destination point can no longer go outside the screen
     * SO YAYYYYY IT WORKS AND STAYS INSIDE THE BOUNDS!
     * 
     * NEXT:
     * get the point to be redone so that the point should be randomly put 
     * somewhere on screen
     */

    [SerializeField] GameObject _point, _test;

    [SerializeField] float _radius, pointTime, moveTime;

    [SerializeField][Range(0f, 90)] float _FOV;

    [SerializeField] Vector2 screenBounds;

    Vector3 destination;

    bool isGenerating = false;

    void Start()
    {
        screenBounds = Camera.main.ScreenToWorldPoint(new Vector3(Screen.width, Screen.height, Camera.main.transform.position.z));
        destination = RandomPointOnCircle(_radius);
        if (CheckPos(_test.transform.position))
        {
            //print("TEST IS INSIDE!");
        }
        else { }
            //print("TEST is not inside T_T");
    }

    void Update()
    {
        StartCoroutine(findDestination(_radius, pointTime));

        // Visually seeing hwere the destination is
        _point.transform.position = destination;
        //Going towards the destination
        transform.position = Vector3.MoveTowards(transform.position, destination, Time.deltaTime * moveTime);
    }

    //RandomPoint works well and generates a point on the circle
    Vector3 RandomPointOnCircle(float radius)
    {
        float angle = Random.Range(0, _FOV);
        float x = Mathf.Cos(Mathf.Deg2Rad * angle) * radius;
        float y = Mathf.Sin(Mathf.Deg2Rad * angle) * radius;
        return new Vector3(x, y);
    }

    IEnumerator findDestination(float radius, float repeatTime)
    {
        // if we aren't already running
        if(!isGenerating)
        {
            //we are now running
            isGenerating = true;

            //return a random point for us
            Vector3 randPoint = RandomPointOnCircle(radius);

            //is the point in the screen?
            //if it isn't break out and run again
            if(!CheckPos(randPoint + transform.position))
            {
                isGenerating = false;
                print("rand point is off screen");
                yield break;
            }

            destination = randPoint + transform.position;

            yield return new WaitForSeconds(repeatTime);
            isGenerating = false;
        }

        yield return null;
    }

    bool CheckPos(Vector3 pos)
    {
        //is it our x bounds
        if (pos.x > -screenBounds.x && pos.x < screenBounds.x)
        {
            //check y bounds
            if (pos.y > -screenBounds.y && pos.y < screenBounds.y)
            {
                return true;
            }
            else
                return false;
        }
        else
            return false;
    }

}
