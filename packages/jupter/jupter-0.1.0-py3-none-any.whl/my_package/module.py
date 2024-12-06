def exp1():
    code="""
                class Stack:
    def __init__(self, max_size):
        self.stack = []
        self.top = -1
        self.MAX = max_size
    
    def isFull(self):
        return self.top == self.MAX - 1
    
    def isEmpty(self):
        return self.top == -1
    
    def push(self, value):
        if self.isFull():
            print("Error: Overflow")
        else:
            self.top += 1
            if len(self.stack) > self.top:
                self.stack[self.top] = value
            else:
                self.stack.append(value)
    
    def pop(self):
        if self.isEmpty():
            print("Stack underflow")
            return None
        else:
            value = self.stack[self.top]
            self.top -= 1
            return value
    
    def display(self):
        if self.isEmpty():
            print("Stack is empty")
        else:
            for i in range(self.top, -1, -1):
                print(self.stack[i], end=" ")
            print()

# Demonstrating stack operations
stack = Stack(5)

print("Pushing values 1, 2, 3")
stack.push(1)
stack.push(2)
stack.push(3)
stack.display()

print("Popping a value:")
stack.pop()
stack.display()

print("Checking for overflow:")
stack.push(4)
stack.push(5)
stack.push(6)
stack.push(7)
stack.display()

print("Checking for underflow:")
while not stack.isEmpty():
    stack.pop()
stack.pop()
"""
    print(code)

def exp1ad():
    code="""class Stack:
    def __init__(self, max_size):
        self.stack = []
        self.top = -1
        self.MAX = max_size
    
    def isFull(self):
        return self.top == self.MAX - 1
    
    def isEmpty(self):
        return self.top == -1
    
    def push(self, value):
        if self.isFull():
            print("Error: Overflow")
        else:
            self.top += 1
            if len(self.stack) > self.top:
                self.stack[self.top] = value
            else:
                self.stack.append(value)
    
    def pop(self):
        if self.isEmpty():
            print("Stack underflow")
            return None
        else:
            value = self.stack[self.top]
            self.top -= 1
            return value
    
    def display(self):
        if self.isEmpty():
            print("Stack is empty")
        else:
            for i in range(self.top, -1, -1):
                print(self.stack[i], end=" ")
            print()

def is_palindrome(string):
    stack = Stack(len(string))
    for char in string:
        stack.push(char)
    
    reversed_string = ""
    while not stack.isEmpty():
        reversed_string += stack.pop()
    
    # Compare the original string with the reversed string character by character
    for i in range(len(string)):
        if string[i] != reversed_string[i]:
            return False
    return True

def palindrome_checker(strings):
    palindrome_stack = Stack(len(strings))
    for string in strings:
        if is_palindrome(string):
            palindrome_stack.push(string)
    print("Palindromes in LIFO order:")
    palindrome_stack.display()

# Test case for palindrome checker
strings = ["radar", "level", "world", "madam"]
palindrome_checker(strings)
"""
   
    code1="""
              def pattern_recognizer(strings, n):
    for string in strings:
        if recognize_pattern_1(string, n):
            print(f"'{string}' matches pattern N(a's) N(b's) any(c's)")
        if recognize_pattern_2(string, n):
            print(f"'{string}' matches pattern N(a's) any(b's) N(c's)")
        if recognize_pattern_3(string, n):
            print(f"'{string}' matches pattern any(a's) N(b's) N(c's)")

def recognize_pattern_1(string, n):
    return string == 'a' * n + 'b' * n + 'c' * len(string[n*2:])

def recognize_pattern_2(string, n):
    b_count = string.count('b')
    return string == 'a' * n + 'b' * b_count + 'c' * n

def recognize_pattern_3(string, n):
    a_count = string.count('a')
    return string == 'a' * a_count + 'b' * n + 'c' * n

# Test cases for pattern recognizer
strings = ["aaaabbbbcc", "aaaabbbccc", "aabbbccc"]
n = 4
pattern_recognizer(strings, n)
""" 
    print(code)
    print()
    print(code1)

def exp2():
    code="""
          class stackadt:
    def __init__(self,size):
        self.stack1=[None]*size
        self.post=[None]*size
        self.top=-1
        self.postindex=0
    def push(self,element):
        self.top=self.top+1
        self.stack1[self.top]=element
    
    def pop(self):
        if(self.top==-1):
            print("the stack is empty")
            return
        else:
            element=self.stack1[self.top]
            self.top=self.top-1
            return element

    def conversion(self,data):
        for i in data:
            if i=='(':
                self.push(i)
            elif i.isalpha():
                self.post[self.postindex]=i
                self.postindex+=1
            elif i in "+-*/":
                while((self.stack1[self.top]!=1 and self.stack1[self.top]!='(') and (
                   ( i in "+-" and self.stack1[self.top] in "+-/*") or (i in "*/" and self.stack1[self.top] in "*/"))):
                    self.post[self.postindex]=self.pop()
                    self.postindex+=1
                self.push(i)
            elif i ==')':
                while(self.stack1[self.top]!=-1 and self.stack1[self.top]!='('):
                    self.post[self.postindex]=self.pop()
                    self.postindex+=1
                self.pop() # to remove the (
            else:
                pass 
        
        while self.top!=-1:
            self.post[self.postindex]=self.pop()
            self.postindex+=1
        
        for i in range(self.postindex):
            print(self.post[i],end='')
        

stack1=stackadt(10)
stack1.conversion("(A+B)")
"""
    print(code)
def exp2ad():
    code="""
class stackat:
    def __init__(self,size):
        self.stack1=[None]*size
        self.top=-1
        self.size=size
    def push(self,element):
        if(self.top==self.size-1):
            print("the stack is full")
            return
        self.top=self.top+1
        self.stack1[self.top]=element
    def pop(self):
        if(self.top==-1):
            print("the stack is empty")
            return
        self.top=self.top-1

    def check(self,exp):
        for i in exp:
            if i in '(':
                self.push(i)
            elif i in ')':
                if(self.top==-1):
                    print("unbalanced paranthesis")
                    return 1
                self.pop()
                
        return self.top

st=stackat(5)
x=st.check("((A+B))")
print(x)
if(x==-1):
    print("balanced paranthesis")
if(x>=0):
    print("unbalanced paranthesis")"""
    print(code)

def exp3():
    code="""# queue implementation

class qeue:
    def __init__(self,size):
        self.size=size
        self.front=-1
        self.rear=-1
        self.stack1=[None]*size
    def is_full(self):
        return self.rear==self.size-1
    def is_empty(self):
        return self.front==-1
    def enqeue(self,element):
        if self.is_full():
            print("the stack is full")
            return 
        self.rear=self.rear+1
        if(self.front==-1):
            self.front=0
        self.stack1[self.rear]=element
    def deqeue(self):
        if self.is_empty():
            print("the stack is empty")
            return
        element=self.stack1[self.front]
        if(self.front==self.rear):
            self.front=self.rear=-1
        else:
            self.front=self.front+1
        print("the element popped is:",element)
    def display(self):
        if(self.front!=-1):
            for i in range(self.front,self.rear+1):
                print(self.stack1[i])

q=qeue(4)
q.enqeue(1)
q.enqeue(2)
q.enqeue(3)
q.enqeue(4)


q.deqeue()
q.deqeue()
q.deqeue()
q.deqeue()


q.display()
              """
    print(code)





def exp7ad():
    code="""
// Online Java Compiler
// Use this editor to write, compile and run your Java code online

import java.util.Scanner;
class Node{
    Node next;
    char data;
    Node(char data){
        this.data=data;
        this.next=null;
    }
}


class  linkedstack{
    Node top;
    public void push(char data){
        Node newnode=new Node(data);
        newnode.next=top;
        top=newnode;
    }
    
    public char pop(){
        if(top==null){
            System.out.println("the stack is empty");
            return '*';
        }
        char data=top.data;
        Node temp=top;
        top=top.next;
        temp=null;
        return data;
    }
    public void display(){
          if(top==null){
            System.out.println("the stack is empty");
            return;
        }
        Node temp=top;
        while(temp!=null){
            System.out.print(temp.data+"->");
            temp=temp.next;
        }
        System.out.print("null");
    }
}

class linkedqeue{
    Node front,rear;
    
    public void enqeue(char data){
        Node newnode=new Node(data);
        if(front==null){
            front=rear=newnode;
        }
        rear.next=newnode;
        rear=newnode;
    }
    
    public char dequeue(){
        if(front==null){
            System.out.println("the queue is empty");
            return '*';
        }
        char data=front.data;
        Node temp=front;
        front=front.next;
        temp=null;
        return data;
    
    }
    
    public void display(){
        if(front==null){
            System.out.println("the queue is empty");
            return;
        }
        Node current=front;
        while(current!=null){
            System.out.print(current.data+"->");
            current=current.next;
        }
        System.out.print("null");
    }
}
class Main {
    public static void main(String[] args) {
        
        
        linkedstack ls=new linkedstack();
        linkedqeue lq=new linkedqeue();
        Scanner sr=new Scanner(System.in);
        System.out.println("Enter the name:");
        String name=sr.next();
        for (int i=0;i<name.length();i++){
            ls.push(name.charAt(i));
            lq.enqeue(name.charAt(i));
        }
        int flag=0;
        for(int i=0;i<name.length();i++){
            char data1=ls.pop();
            char data2=lq.dequeue();
            if(data1!=data2){
                flag=1;
                System.out.println("the string is not palindrome");
                break;
            }
    }
    
     if (flag==0){
         System.out.println("the string is palindrome");
     }
     }
}"""

    print(code)

    code1="""
# decimal to bianry using linked stacl

class Node:
    def __init__(self,data):
        self.data=data 
        self.next=None

class linkedstack:
    def __init__(self):
        self.top=None
    def is_empty(self):
        return self.top==None
    
    def push(self,data):
        node=Node(data)
        node.next=self.top
        self.top=node
    def pop(self):
        if not self.is_empty():
            data=self.top.data
            self.top=self.top.next
            return data
        else:
            print("Empty stack")
def binary(data):
    ls=linkedstack()
    c=-1
    while(data>0):  
        reminder=data%2
        ls.push(reminder)
        data=data//2
        c=c+1
    s1=""
    while not ls.is_empty():
        s=(str)(ls.pop())
        s1=s1+s
    return s1


print(binary(23))"""
    print(code1)

def exp8():
    code="""
        

class search:
    def __init__(self,data):
        self.data=data

    def linear(self,element):
        flag=0
        for i in self.data:
            if(i[1]==element):
                flag=1
                print(f"the data is found and it is:{i}")
        if flag!=1:
            print("the data is not found")
    def binary(self,element):
        l1=[None]*len(self.data)
        k=0
        for i in self.data:
            l1[k]=i[0]
            k=k+1

        low=0
        high=len(l1)-1
        flag=0
        while(low<=high):
            mid=(low+high)//2

            if(l1[mid]==element):
                flag=1
                print("the element is found and it is:",self.data[mid])
                break

            elif(l1[mid]<element):
                low=mid+1
            else:
                high=mid-1
        if flag!=1:
            print("the data is not present")
    




database=[(1,"eggs"),(2,"jam"),(3,"kellogs")]
s=search(database)
s.linear("egg")
s.binary(2)"""
    print(code)


def exp9():
    code="""
       # hash table

class hashtable:
    def __init__(self,size):
        self.size=size
        self.hash=[None]*size
    
    def index_cal(self,element):
        index=element%self.size
        #print(index)
        if(self.hash[index] is None):
            return index
        else:
             #linear probing
             current=index
             while(current is not None):
                 current=(current+1)%self.size
                 if(self.hash[current] is None):
                     return current
                 if(current==index):
                     #print("the hashtble is full")
                     return -1

    def insert(self,element):
        index=self.index_cal(element)
        if(index!=-1):
            self.hash[index]=element
        else:
            print("the hashtble is full")
    def search(self,element):
         index=element%self.size
         if(self.hash[index]  ==element):
             print("the element is found at index",index)
         else:
             current=index
             while(current is not None):
                 if(self.hash[current] ==element):
                     print("the element is found at index",current)
                     break
                 else:
                     current=(index+1)%self.size
                 if(current==index):
                     print("the element is not present in the table")
                     break
    def display(self):
        for i in range(self.size):
            print(self.hash[i])


hs=hashtable(3)
hs.insert(1)
hs.insert(4)
hs.insert(5)
#hs.search(5)

hs.search(4)
hs.display()

"""
    print(code)

def exp6():
    code="""
         // Online Java Compiler
// Use this editor to write, compile and run your Java code online
class Node{
    int data;
    Node next;
    Node prev;
    Node(int data){
        this.data=data;
        this.next=null;
        this.prev=null;
    }
}

class doublelinked{
    Node head;
    Node tail;
    
    public void insertatbeg(int data){
        Node newnode=new Node(data);
        if(head==null){
            head=tail=newnode;
        }
        else{
            newnode.next=head;
            head.prev=newnode;
            head=newnode;
        }
    }
    
    public void insertatend(int data){
        Node newnode=new Node(data);
        if(head==null){
            head=tail=newnode;
        }
        else{
            tail.next=newnode;
            newnode.prev=tail;
            tail=newnode;
        }
    }
    
    public void insertafter(int data,int key){
        Node temp=head;
        while(temp!=null && temp.data!=data){
            temp=temp.next;
        }
        
        if(temp==null){
            System.out.println("the list is empty");
            
            return;
        }
        Node newnode=new Node(key);
        if(data==tail.data){
            tail.next=newnode;
            newnode.prev=tail;
            tail=newnode;
        }
        else{
            newnode.next=temp.next;
            newnode.prev=temp;
            
            if(temp.next!=null){
                temp.next.prev=newnode;
            }
            temp.next=newnode;
        }
        
    }
    
    public void deleteatbeg(){
        if(head!=null){
            head=head.next;
            head.prev=null;
        }
        else{
            System.out.println("the list is empty");
        }
    }
    
    public void deleteatend(){
        if(tail!=null){
            tail=tail.prev;
            tail.next=null;
        }
    }
    
    public void deleteafter(int key){
        if(head.data==key){
            head=head.next;
            head.prev=null;
            return;
        }
        Node temp=head;
        while(temp!=null && temp.data!=key){
            temp=temp.next;
        }
        if(temp.next.next!=null){
            temp.next.next.prev=temp;
        }
        temp.next=temp.next.next;
        
    }
  
  
    public void display(){
        Node temp=head;
        while(temp!=null){
            System.out.print(temp.data+"<->");
            temp=temp.next;
        }
    }
}
class Main {
    public static void main(String[] args) {
        
        doublelinked ls=new doublelinked();
        
        ls.insertatbeg(4);
        ls.insertatbeg(2);
        ls.insertatbeg(3);
        ls.insertatbeg(1);
        
        //ls.insertafter(4,6);
        
        //ls.insertatend(5);
        
        
        //ls.deleteatbeg();
      // ls.deleteatend();
     //  ls.deleteafter(3);
     
        ls.display();
    }
}""" 
    print(code)

def exp4():
    code="""#circular queue

class circular:
    def __init__(self,size):
        self.size=0
        self.front=-1
        self.rear=-1
        self.capacity=size
        self.qeue=[None]*size
    def is_empty(self):
        return (self.size==0)
    
    def is_full(self):
        return (self.capacity==self.size)
    
    def enqeue(self,element):
        if self.is_full():
            print("the qeue is full")
            return
        self.rear=(self.rear+1)%self.capacity
      #if(self.front==-1):
         #   self.front=0
        self.qeue[self.rear]=element
        self.size=self.size+1
    def deqeue(self):
        if self.is_empty():
            print("the queue is empty")
            return
        front=(front+1)%self.capacity
        data=self.qeue[self.front]
        front=(front+1)%self.capacity
        print("the data is removed is ",data)
        self.size=self.size-1

    def display(self):
       # print(self.size)
        for i in range(self.size):
            print(self.qeue[i],end=",")

cq=circular(3)

cq.enqeue(1)
cq.enqeue(2)
cq.enqeue(3)

cq.display()"""
    print(code)


def exp5():
    code ="""
          // Online Java Compiler
// Use this editor to write, compile and run your Java code online
// singly i


class Node {
    int data;
    Node next;
    Node(int data){
        this.data=data;
        this.next=null;
    }
}
class singlelinked{
    Node head;
    
    public void insertatbeg(int data){
        
        Node newnode=new Node(data);
        if(head==null){
            head=newnode;
            return;
        }
        newnode.next=head;
        head=newnode;
    }
    
    public void insertatend(int data){
        Node newnode=new Node(data);
        
        Node temp=head;
        while(temp!=null && temp.next!=null){
            temp=temp.next;
        }
        temp.next=newnode;
        temp=newnode;
    }
    
    public void insertafter(int data,int key){
        Node newnode=new Node(key);
        if(head.data==data){
            newnode.next=head.next;
            head.next=newnode;
            return ;
            
        }
        Node temp=head;
        while(temp!=null && temp.data!=data){
            temp=temp.next;
        }
        
        if(temp==null){
            System.out.println("the element not present in the list");
            return;
            
        }
        
        newnode.next=temp.next;
        temp.next=newnode;
        
    }
    
    
    public void display(){
        Node temp=head;
        while(temp!=null){
            System.out.print(temp.data+"->");
            temp=temp.next;
        }
        
    }
    
    public void deleteatbeg(){
        if(head.next!=null){
            head=head.next;
        
            return;
        }
        head=null;
        
    }
    
    public void deleteatend(){
        Node temp=head;
        while(temp!=null && temp.next.next!=null){
            temp=temp.next;
        }
        
        temp.next=temp.next.next;
        
    }
    
    public void deleteafter(int data){
        Node temp=head;
        while(temp!=null && temp.data!=data){
            temp=temp.next;
        }
        temp.next=temp.next.next;
        
    }
}
class Main {
    public static void main(String[] args) {
        
        singlelinked ls=new singlelinked();
        ls.insertatbeg(4);
        ls.insertatbeg(5);
        ls.insertatbeg(6);
        ls.insertatend(7);
        ls.insertafter(6,8);
        //ls.deleteatbeg();
       //ls.deleteatend();
       
       ls.deleteafter(5);
       l
        ls.display();
    }
}"""
    
    print(code)


def exp10():
    code=""""
       class Node:
    def _init_(self,data):
        self.data = data
        self.rchild = None
        self.lchild = None
class BST:
    def _init_(self):
        self.root = None
    def insert(self,data):
        self.root = self.insert_rec(self.root,data)
    def insert_rec(self,root,data):
        if root is None:
            return Node(data)
        if data < root.data:
            root.lchild = self.insert_rec(root.lchild,data)
        elif data > root.data:
            root.rchild = self.insert_rec(root.rchild,data)
        return root
    def pre_order(self,node):
        if node:
            print(node.data,end=' ')
            self.pre_order(node.lchild)
            self.pre_order(node.rchild)
    def in_order(self,node):
        if node:
            self.in_order(node.lchild)
            print(node.data,end=' ')
            self.in_order(node.rchild)
    def post_order(self, node):
        if node:
            self.post_order(node.lchild)
            self.post_order(node.rchild)
            print(node.data,end=' ')
    def level_order(self):
        height = self.get_height(self.root)
        for i in range(1,height+1):
            self.print_current_level(self.root,i)
    def level_order(self):
        height = self.get_height(self.root)
        for i in range(1,height+1):
            self.print_current_level(self.root,i)
    def get_height(self,root):
        if root is None:
            return 0
        left_height = self.get_height(root.lchild)
        right_height = self.get_height(root.rchild)
        return max(left_height,right_height)+1
    def print_current_level(self,root,level):
        if root is None:
            return 
        elif level == 1:
            print(root.data,end=" ")
        elif level > 1:
            self.print_current_level(root.lchild,level-1)
            self.print_current_level(root.rchild,level-1)

bst = BST()
bst.insert(5)
bst.insert(4)
bst.insert(6)
bst.pre_order(bst.root)
bst.in_order(bst.root)
bst.post_order(bst.root)
bst.level_order()"""
        
    print(code)