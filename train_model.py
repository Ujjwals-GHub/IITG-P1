from ultralytics import YOLO

def main():
    model = YOLO("yolo11n.pt")
    model.train(data="model.yaml", epochs=100, imgsz=640, workers=0)

if __name__ == "__main__":
    main()