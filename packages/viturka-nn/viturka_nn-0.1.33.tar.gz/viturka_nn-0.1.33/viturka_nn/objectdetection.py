import torch
from torch.utils.data import DataLoader, Dataset
from torchvision.models.detection import ssdlite320_mobilenet_v3_large
from torch import nn
import torchvision.transforms as T
from torchvision.ops import box_iou
from torchvision.datasets import CocoDetection
from PIL import Image
import os
from pycocotools.coco import COCO

class ObjectDetection:
    def __init__(self, num_classes=6, pretrained=True, device="cuda"):
        self.num_classes = num_classes
        self.device = device
        self.model = ssdlite320_mobilenet_v3_large(pretrained=pretrained)

        # Modify the classification head for custom classes
        if num_classes != 91:
            self.model.head.classification_head.num_classes = num_classes

        # Replace BatchNorm with GroupNorm
        self.model = self._replace_batchnorm_with_groupnorm(self.model)
        self.model.to(self.device)

        # Default class names as placeholders
        self.class_names = [f"class_{i}" for i in range(num_classes)]

    def set_class_names(self, class_names):
        """Sets class names from a list."""
        if len(class_names) != self.num_classes:
            raise ValueError(f"Length of class_names must be {self.num_classes}")
        self.class_names = class_names

    def _replace_batchnorm_with_groupnorm(self, model):
        layers_to_replace = []
        for name, module in model.named_modules():
            if isinstance(module, nn.BatchNorm2d):
                num_features = module.num_features
                layers_to_replace.append((name, nn.GroupNorm(num_groups=4, num_channels=num_features)))

        for name, new_layer in layers_to_replace:
            *parent_path, layer_name = name.split('.')
            parent_module = model
            for p in parent_path:
                parent_module = getattr(parent_module, p)
            setattr(parent_module, layer_name, new_layer)

        return model

    def _default_transforms(self):
        return T.Compose([
            T.Resize((320, 320)),
            T.ToTensor(),
            T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

    def load_data(self, images_dir, annotation_file, batch_size=4, transforms=None):
        if transforms is None:
            transforms = self._default_transforms()

        dataset = CustomDataset(root_dir=images_dir, annotation_file=annotation_file, transforms=transforms)
        self.dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True, collate_fn=lambda x: tuple(zip(*x)))
        return self.dataloader

    def train(self, num_epochs=10, lr=0.005):
        optimizer = torch.optim.SGD(self.model.parameters(), lr=lr, momentum=0.9, weight_decay=0.0005)
        for epoch in range(num_epochs):
            self.model.train()
            total_loss = 0.0
            for images, targets in self.dataloader:
                images = [img.to(self.device) for img in images]
                targets = [{k: v.to(self.device) for k, v in t.items()} for t in targets]

                optimizer.zero_grad()
                loss_dict = self.model(images, targets)
                loss = sum(loss for loss in loss_dict.values())
                loss.backward()
                optimizer.step()
                total_loss += loss.item()

            print(f"Epoch [{epoch + 1}/{num_epochs}], Loss: {total_loss / len(self.dataloader):.4f}")

    def evaluate(self):
        self.model.eval()
        metrics = {
            'iou': [],
            'precision': [],
            'recall': [],
            'f1_score': []
        }

        with torch.no_grad():
            for images, targets in self.dataloader:
                images = [img.to(self.device) for img in images]
                preds = self.model(images)

                batch_metrics = self._calculate_metrics(preds, targets)
                for key, value in batch_metrics.items():
                    metrics[key].append(value)

        averaged_metrics = {k: sum(v) / len(v) for k, v in metrics.items()}
        return averaged_metrics

    def _calculate_metrics(self, preds, targets):
        ious, precisions, recalls, f1_scores = [], [], [], []

        for pred, target in zip(preds, targets):
            pred_boxes = pred['boxes'].to(self.device)
            pred_labels = pred['labels'].to(self.device)
            target_boxes = target['boxes'].to(self.device)
            target_labels = target['labels'].to(self.device)

            iou_matrix = box_iou(pred_boxes, target_boxes)
            iou_threshold = 0.5

            matched_preds = iou_matrix > iou_threshold
            true_positives = matched_preds.sum().item()
            false_positives = len(pred_labels) - true_positives
            false_negatives = len(target_labels) - true_positives

            avg_iou = iou_matrix[matched_preds].mean().item() if matched_preds.sum() > 0 else 0
            precision = true_positives / (true_positives + false_positives + 1e-6)
            recall = true_positives / (true_positives + false_negatives + 1e-6)
            f1_score = 2 * (precision * recall) / (precision + recall + 1e-6)

            ious.append(avg_iou)
            precisions.append(precision)
            recalls.append(recall)
            f1_scores.append(f1_score)

        return {
            'iou': sum(ious) / len(ious),
            'precision': sum(precisions) / len(precisions),
            'recall': sum(recalls) / len(recalls),
            'f1_score': sum(f1_scores) / len(f1_scores)
        }

class CustomDataset(Dataset):
    def __init__(self, root_dir, annotation_file, transforms=None):
        self.root_dir = root_dir
        self.coco = COCO(annotation_file)
        self.transforms = transforms
        self.ids = list(self.coco.imgs.keys())

    def __getitem__(self, index):
        img_id = self.ids[index]
        annotation_ids = self.coco.getAnnIds(imgIds=img_id)
        annotations = self.coco.loadAnns(annotation_ids)

        boxes = [ann['bbox'] for ann in annotations]
        labels = [ann['category_id'] for ann in annotations]
        boxes = torch.as_tensor(boxes, dtype=torch.float32)
        boxes[:, 2:] += boxes[:, :2]

        img_path = os.path.join(self.root_dir, self.coco.imgs[img_id]['file_name'])
        image = Image.open(img_path).convert("RGB")
        target = {'boxes': boxes, 'labels': torch.tensor(labels, dtype=torch.int64)}

        if self.transforms:
            image = self.transforms(image)

        return image, target

    def __len__(self):
        return len(self.ids)


import torch
import torchmetrics
from torchvision.models.detection import ssdlite320_mobilenet_v3_large
from typing import Optional
from torchmetrics.detection.mean_ap import MeanAveragePrecision


class ModelHandler:
    def __init__(self, model: Optional["ObjectDetection"] = None, model_path: str = "saved_model.pth"):
        """
        Initializes the ModelHandler.
        If a model is provided, it will be used for saving; otherwise, it will assume an already saved model.

        :param model: (Optional) ObjectDetection model instance to save or evaluate.
        :param model_path: Path where the model is saved or will be saved.
        """
        self.model = model
        self.model_path = model_path

    def save_model(self):
        """
        Saves the model to the specified path.
        """
        if self.model is None:
            raise ValueError("No model provided for saving.")

        torch.save(self.model.state_dict(), self.model_path)
        print(f"Model saved to {self.model_path}.")

    def load_model(self, num_classes=6, device='cuda'):
        """
        Loads a model from the specified path.

        :param num_classes: Number of classes in the model's classification head.
        :param device: Device to load the model on ('cpu' or 'cuda').
        """
        self.model = ObjectDetection(num_classes=num_classes, pretrained=False, device=device)
        self.model.model.load_state_dict(torch.load(self.model_path, map_location=torch.device(device)))
        self.model.model.eval()
        print(f"Model loaded from {self.model_path}.")

    def load_test_data(self, test_data_path: str, annotation_file: str, batch_size: int = 4):
        """
        Loads a test dataset for evaluation.

        :param test_data_path: Path to the folder containing test images.
        :param annotation_file: Path to the COCO annotation JSON file for test images.
        :param batch_size: Batch size for the DataLoader.
        """
        transform = T.Compose([
            T.ToTensor(),
            T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

        test_dataset = CocoDetection(root=test_data_path, annFile=annotation_file, transform=transform)
        self.dataloader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, collate_fn=self._collate_fn)
        print(f"Test dataset loaded from {test_data_path} with annotations {annotation_file}.")

    def _collate_fn(self, batch):
        """
        Custom collate function to handle variable image sizes and annotations.
        """
        images, targets = zip(*batch)
        return list(images), list(targets)

    def evaluate_model(self, test_dataset, device="cuda"):
        self.model.eval()
        ious, precisions, recalls, f1_scores = [], [], [], []

        with torch.no_grad():
            for images, targets in self.dataloader:  # Ensure you're using DataLoader here
                images = [img.to(device) for img in images]

                # Forward pass through the model
                preds = self.model(images)

                # Calculate metrics for each image in the batch
                for pred, target in zip(preds, targets):
                    pred_boxes = pred["boxes"].to(device)
                    pred_labels = pred["labels"].to(device)

                    target_boxes = target["boxes"].to(device)
                    target_labels = target["labels"].to(device)

                    iou_matrix = box_iou(pred_boxes, target_boxes)
                    iou_threshold = 0.5

                    matched_preds = iou_matrix > iou_threshold
                    true_positives = matched_preds.sum().item()
                    false_positives = len(pred_labels) - true_positives
                    false_negatives = len(target_labels) - true_positives

                    avg_iou = iou_matrix[matched_preds].mean().item() if matched_preds.sum() > 0 else 0
                    precision = true_positives / (true_positives + false_positives + 1e-6)
                    recall = true_positives / (true_positives + false_negatives + 1e-6)
                    f1_score = 2 * (precision * recall) / (precision + recall + 1e-6)

                    ious.append(avg_iou)
                    precisions.append(precision)
                    recalls.append(recall)
                    f1_scores.append(f1_score)

        avg_metrics = {
            'iou': sum(ious) / len(ious),
            'precision': sum(precisions) / len(precisions),
            'recall': sum(recalls) / len(recalls),
            'f1_score': sum(f1_scores) / len(f1_scores)
        }
        return avg_metrics

