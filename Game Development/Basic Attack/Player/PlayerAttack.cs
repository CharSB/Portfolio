using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Linq;

public class PlayerAttack : MonoBehaviour
{
    [SerializeField] LayerMask Attackable;
    [SerializeField] List<GameObject> inRange = new List<GameObject>();

    private void Update()
    {
        if (Input.GetKeyDown(KeyCode.C))
        {
            if (inRange.Count != 0)
            {
                Attack(CalcNearest(inRange));
            }
        }
    }

    #region Detecting Enemies

    private void OnTriggerEnter2D(Collider2D collision)
    {
        Transform enemyTransform = collision.transform;
        RaycastHit2D hit2D = Physics2D.Linecast(transform.position, enemyTransform.position, Attackable);
        if (inRange.Contains(hit2D.collider.gameObject) == false)
        {
            inRange.Add(hit2D.collider.gameObject);
        }
    }

    private void OnTriggerExit2D(Collider2D collision)
    {
        GameObject enemy = collision.gameObject;
        if (inRange.Contains(enemy))
        {
            inRange.Remove(enemy);
        }
    }

    #endregion

    [SerializeField] float attackTime = .5f;
    private void Attack(GameObject enemy)
    {
        transform.position = Vector3.Lerp(transform.position, enemy.transform.position, attackTime);
        Destroy(enemy);
    }

    private GameObject CalcNearest(List<GameObject> gameObjects)
    {
        GameObject nearest = gameObjects[0];
        float shortty;
        //save time when only 1 object
        if (gameObjects.Count != 1)
        {
            List<float> distances = new List<float>();

            //find distance from player for all objects
            for (int i = 0; i < gameObjects.Count - 1; i++)
            {
                GameObject gameObject = gameObjects[i];
                Vector3 distance = gameObject.transform.position - transform.position;
                distances.Add(distance.magnitude);
            }

            shortty = distances.Min();

            for(int i = 0; i < distances.Count - 1; i++)
            {
                if(distances[i] == shortty)
                {
                    nearest = gameObjects[i];
                }
            }
        }
        return nearest;
    }

}

    
        

