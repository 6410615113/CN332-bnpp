using System;
using System.Collections.Generic;

// Subscriber Interface
interface ISubscriber
{
    void Update(string msg);
}


class Student : ISubscriber
{
    public void Update(string msg)
        => Console.WriteLine($"Student receive new message, {msg}");
}
class Teacher : ISubscriber
{
    public void Update(string msg)
        => Console.WriteLine($"Teacher receive new message, {msg}");
}

// Publisher
class SchoolMessager
{
    private IList<ISubscriber> subscribers;

    public SchoolMessager()
        => subscribers = new List<ISubscriber>();

    public void Subscribe(ISubscriber newSubscriber)
        => subscribers.Add(newSubscriber);
    
    public void Unsubscribe(ISubscriber newSubscriber)
        => subscribers.Remove(newSubscriber);

    public void SendMessage(string msg)
    {
        foreach(var it in subscribers)
        {
            it.Update(msg);
        }
    }
}

// Client
class Program
{
    static void Main(string[] args)
    {
        var student = new Student();
        var teacher = new Teacher();

        var publisher = new SchoolMessager();
        publisher.Subscribe(student);
        publisher.Subscribe(teacher);

        Console.WriteLine("Annoucement from university: ");
        publisher.SendMessage("Today isn't have a class");

        Console.WriteLine("Student want to unsubscribe a message");
        publisher.Unsubscribe(student);

        Console.WriteLine("Annoucement from university: ");
        publisher.SendMessage("already unsubscribed");
    }
}
