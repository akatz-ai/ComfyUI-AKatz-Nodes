# AKatz Nodes

### AK Dilate Mask Linear

Dilates a mask in a linear animated fashion given a mask batch.
- mask: MASK, input a mask batch
- shape: "circle" or "square", "circle" is the most accurate and should be used for final renders. "square" is fast to calculate and should be used for testing the workflow.
- dilate_per_frame: INT, how much the mask should be dilated per frame.
- delay: INT, number of frames to wait before starting dilation.