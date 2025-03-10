# EasyLabeler

<div align="center">

<h1>EasyLabeler</h1>

EasyLabeler: An open-source intelligent video annotation tool. Maintained by [EasySort](https://github.com/Easysort).
</div>

---

To clone: ```git clone --recurse-submodules https://github.com/Easysort/easylabeler```

# What is EasyLabeler
EasyLabeler makes the process of annotating videos as easy as possible. It has multiple AI features to help you annotate faster and automate processes as quickly as possible.

# How to setup EasyLabeler

Run using:

```
PYTHONPATH="Easysort" python main.py
```

# How to use:

Space: Play/Pause
H, J, K, L: Skip -5, -1, 1, 5 frames
W, S: Move class id up, down
A, D: Move class id fraction up, down

Add detections by pressing on image. (ESC to cancel)
Change detection by holding on the corners. 
Highlight detections by clicking on a corner of the detection. (ESC to unhighlight)
Right click on a corner to delete a detection

# Fully open-source
You can use EasyLabeler as you like, copy it, modify it, sell it, do whatever you like with it. The project is in active development, so issues and pull requests are welcome.

- [x] Refactor detections and bbox
- [x] Be able to load detections
- [x] Be able to add detections
- [x] Be able to modify detections
- [x] Be able to delete detections
- [x] Be able to visualize detections
- [ ] Be able to run Yolos
- [ ] Interpolation
- [x] Be able to change class_ids
- [x] Be able to focus detection
- [x] Be able to modify detection corners
- [ ] Readme
- [ ] Should be able to have the same track_id for different detections in different frames (max 1 in each frame)