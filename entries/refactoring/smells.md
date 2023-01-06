Code smells from mild to Strong

Code smells are something all developers deal with. We want to make sure you are aware of them. Let’s learn what they are and how to stop them.

If Stupidity got us into this mess, then why can’t it get us out?
Will Rogers

I can remember some of my earliest Java code I wrote. It was pretty gnarly stuff. Once someone mentioned code smells and I read a little bit I knew I was a major violator!

Code Smells
According to Wikipedia a Code Smell is:

In computer programming, a code smell is any characteristic in the source code of a program that possibly indicates a deeper problem.

This article details some of the basic code smells. I would assume at one time or another I have made all of these mistakes.

Bloaters
Cory was a character that I worked with many years ago. He liked to poke fun at mistakes others had made. There was one class that had been touched by many hands and grow to the size of a novel. He printed out the file and taped it together outside of his cube. It got people’s attention but he didn’t win many friends. This was an example of a “Bloater”. We start with good intentions and then someone adds a few lines here and there. Soon it is has grown too big! This can be a large class or a super long method.

OO Abusers
The Java language has the switch statement. For object-oriented design, it is usually a sign of lazy design. It is better to remove it and create a method to handle this. Another option is to replace the type code with the subclass. This can be a great place to use polymorphism to handle the changes.

Change Preventers
One of my first duties as a professional developer was to make changes to an order entry system. The original developer had made most tasks flow through one very large program. It was so unwieldy that the person who was guiding at the time said don’t touch that main program. It was so large it was a change preventer. Everyone was scared to touch anything for the fact of what might happen.

Dispensables
If you have ever seen an episode of the A&E Network show Hoarders you will understand what dispensables are in code. Programmers can be reluctant to delete code. Think of this as a digital packrat! When a feature is no longer used we need to delete it, not keep it around like artwork.

Couplers
My wife likes to watch the Bachelor on ABC. They have a formula of ladies who get intimate with the Bachelor then cause drama amongst the contestants. If your classes need to share too much information with each other it might be time to refactor. Come on keep it professional, please.

Every developer spends a lot of time on Stackoverflow.com. One of the founders Jeff Atwood who occasionally blogs at CodingHorror shared some good recommendations on code smells as well.

Comments
Jeff brings up some great questions regarding comments. I see this in many codebases. Some refactoring could eliminate the need for some comments.

Long Method
We touched on this before but it bears repeating. Methods need to be succinct and to the point. Name your method something and just do that! Don’t add a few other things it is probably best to create a new one instead.

Duplicated Code
This is a personal favorite of mine. I worked at a company once that had the same method in 142 different places in the same codebase. I was blown away! Put it in one place and Don’t Repeat Yourself! (aka DRY principle)

So if you are a coder you should be aware of the issues that code smells indicate. There may be times when you can knowingly violate one of these. Of course, be careful what mess you leave behind for our fellow developers.

What code smells have you seen?