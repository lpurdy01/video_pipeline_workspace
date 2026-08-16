# FAA AC 20-115D Source Note

## Provenance

raw_file: refrence_literature/raw/extracted_markdown/faa_ac_20_115d.txt
raw_url: https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_20-115D.pdf
summary_method: llm-extract-from-raw
summary_verified: false

## Source

FAA Advisory Circular 20-115D, `Airborne Software Development Assurance Using EUROCAE ED-12( ) and RTCA DO-178( )`, dated July 21, 2017.

Local files:

- `refrence_literature/raw/pdfs/faa_ac_20_115d.pdf`
- `refrence_literature/raw/extracted_markdown/faa_ac_20_115d.txt`

Public URL:

https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_20-115D.pdf

## Why It Matters

This is a public FAA document that can substitute for direct DO-178C access when the whitepaper needs an official statement about DO-178C, DO-330, and related supplements being recognized in certification guidance.

## Key Ideas

- The AC recognizes RTCA DO-178C, DO-330, DO-331, DO-332, and DO-333, along with equivalent EUROCAE documents.
- ED-12C/DO-178C is identified as an acceptable means of compliance for software aspects of type certification or TSO authorization.
- Use of ED-12C/DO-178C implies satisfying applicable objectives and producing associated life cycle data.
- Section 12.2 of ED-12C/DO-178C and ED-215/DO-330 provide an acceptable method for tool qualification.
- DO-330 is described as containing objectives, activities, and life cycle data for tool qualification.

## Useful Claims

- DO-178C can be discussed through public FAA recognition without copying or redistributing the licensed standard.
- Assurance arguments in this project should emphasize objective satisfaction and life cycle evidence, not just final test results.
- Tool qualification has its own objective/data structure and is not merely a casual confidence statement.

## Requirements Impact

- The verification compiler should produce life-cycle-style evidence records for claims and checks.
- Model/tool qualification records should include objective, activity, and evidence fields.
- The project should maintain source provenance for each claim because some primary standards are not redistributable.

## Follow-Up Questions

- Which FAA AC passages should be cited in the public whitepaper versus held as background source notes?
- Should the whitepaper explicitly state that DO-178C itself is licensed and therefore represented by FAA/NASA public guidance?
