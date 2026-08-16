The goal of this project is to researching agentic structuring such that we can 
improve the usage of agents in safety critical software engineering.


In safety critical software there is a lot of human time spent in the verification
stage. In this workspace we are going to work towards building a verification-validation
pipeline that can allow software development to be verified against its specificaiton
in a workflow while minimizing human interactions in metnous tasks.


English as a language is non specific for a medium to specify software interactions.
It is an interesting requirement to even have the concept of an english language specificaiton.
We will probably expand on this at some point.


The initial idea for this project comes from a concept where we are working with units of 
intelegence. 

Units of intelegence have several properties:
- capacity (something akin to short term memory / context window)
- accuracy (this has several forms, and is a function of window)
- adaptability (intelegence seems to come in layers. I like the analogy that when building 
a foundation model it is more like recreating all the components of human brain evolution, 
rather than a brain adapting. Brains come with a lot of prebuilt stuff in them, so the rate that a
human can adapt and learn is much faster. This came from Dario (CEO of Anthropic, likely a citation can
be found in one of his books))
- 

It was recently discovered (likely a citation can be found for this) that with latest agentic development
practice, because the capacity of units of intelegence is limited subdividing tasks and specailzing is
a good way to allow systems of units of intelegence to accomplish more than they would otherwise be able to
through collaboration. This is essentially hierarchies, the same thing we see in companies to accomplish things.
The shape of the hierarchy is important to a company, depening on what kind of the work the company is trying to 
accomplish they may shape their structure much differently.

This is my hypothesis, but I get the feeling that more innovative organizations have generally flatter structures,
where there is still high specialization, but each manager may have 20+ direct reports, and the work is collaborative
between units of intelegence, with everything bringing a unit of expirence and specializaiton.

In more task oriented / managerial structures the nubmer of direct reports is much lower, because the manager's role 
is more involed in verification of correctness rather than innovation.

I am pulling these intuitions from learning about Nvidia's organiztional structure and relating it to what I understand
about professionsal engineers and how many direct reports they may have.


Humans have been working together, as units of intelegence, and we have found and developed many different
systems of collaboration that allows us to specailze into accomplishing tasks most effectively.

One catagory of systems is the concepts necessary for safety software development, or just safety critical engineering
in general. These have several components
- verificaiton and validation
- feedback
- review

There are common organizational / project patterns here, with shared components between
AS9100
DAL level certificaiton
DO-178c based software development
various NASA directives.

Most of these theorize ways to conduct work as units of intelegence within a system to accomplish
work to a standard useful to the system. All of these methods are designed to construct safe products. The work produced
must do what is expected of it without side effects. and errors and updates must be tracked so the next version of the work
doesn't carry known issues forward. There are methods of boards, reporting structures and many other elements designed to
maintain organizational quality.

## Measurment of units of intelegence

In order for engineers to be allowed to wrok on safety critical software they must be 
qualified for the work. Organizations each establish their own methods of this, and it may not
be directly related to creating safe software, but it remains ciritical to the processs.

Often candiates are required to have an accredited education that comprises of many layers of 
tests and educational standards reviewed by boards, then there is an interview process to 
validate engineers further before they join onto teams.

Models and systems of models will required to be verified in some way to ensure that work
delegated is within their qualifications. 

## concept of a validation complier

The concept of a validation compiler is to have a system that with access to a sufficiently qualifed llm for each unit task over an API or some access, can atomically brake down all the
requirements in their  requirements tracability tree as standards like DO-178 describe and
validate the implementation against those requirements.

It is a compiler for DO-178, not the literal complier, but rather the normally human task of validating that the code implemnted meets the spec described.


