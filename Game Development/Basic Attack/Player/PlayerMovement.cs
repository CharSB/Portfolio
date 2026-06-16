using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerMovement : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        Physics2D.queriesStartInColliders = false;
    }

    public void OnDrawGizmos()
    {
        Debug.DrawRay(transform.position, _lastDir, Color.red);
    }

    // Update is called once per frame
    void Update()
    {
        Movement();

        if(Input.GetKeyDown(KeyCode.Space))
        {
            Dash();
        }
    }

    [SerializeField] float speed;
    [SerializeField] float _playerLength;
    private Vector3 _lastDir;
    void Movement()
    {
        float moveX = 0f;
        float moveY = 0f;

        if(Input.GetKey(KeyCode.W))
        {
            moveY = +1f;
        }
        if (Input.GetKey(KeyCode.S))
        {
            moveY = -1f;
        }
        if (Input.GetKey(KeyCode.A))
        {
            moveX = -1f;
        }
        if (Input.GetKey(KeyCode.D))
        {
            moveX = +1f;
        }

        bool isIdle = moveX == 0 && moveY == 0;
        if (isIdle)
        {
            //play idle animation in the _lastDir
        }
        else
        {
            Vector3 moveDir = new Vector2(moveX, moveY).normalized;

            if(TryMove(moveDir, speed * Time.deltaTime))
            {
                //play movement anim (moveDir)
            }
            else
            {
                //play idle anim (_lasDir)
            }
        }
    }

    private bool CanMove(Vector3 dir, float distance)
    {
        return Physics2D.Raycast(transform.position, dir, distance).collider == null;
    }

    private bool TryMove(Vector3 baseMoveDir, float distance)
    {
        Vector3 moveDir = baseMoveDir;
        bool canMove = CanMove(moveDir, distance);
        if (!canMove) //cannot move diagonally
        {
            moveDir = new Vector3(baseMoveDir.x, 0f).normalized;
            canMove = moveDir.x != 0f && CanMove(moveDir, distance);
            if (!canMove) //cannot move horizontally
            {
                moveDir = new Vector3(0f, baseMoveDir.y).normalized;
                canMove = moveDir.y != 0f && CanMove(moveDir, distance);
            }
        }

        if (canMove)
        {
            _lastDir = moveDir;
            transform.position += moveDir * distance;
            return true;
        }
        else
        {
            return false;
        }

    }

    void Dash()
    {
        float dashDistance = 1;
        if (TryMove(_lastDir, dashDistance))
            transform.position += dashDistance * _lastDir;
        else
            print("Can't dash T_T theres an obstacle");
    }
}
