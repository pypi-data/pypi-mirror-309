import torch
import torchvision
from sklearn.preprocessing import label_binarize    
from sklearn.metrics import (
    precision_score, recall_score, f1_score, matthews_corrcoef,
    roc_auc_score, average_precision_score, cohen_kappa_score,
    log_loss
)

# TODO: check if should add range(1) to skip background class
# TODO: check which type of micro, macro, weighted metrics to use
# TODO: test the detection metrics with the torch detection models and yolo
# TODO: add AR and mAR metrics to detection
# TODO: save ROC, PR Curves and confustion metrics values to plot

def get_object_detection_evaluation_results(
    split,
    all_outputs,
    all_targets,
    index_to_labels
):
    """
    Calculate and format object detection evaluation metrics.
    
    Args:
        split: Dataset split type (e.g., 'train', 'val', 'test')
        all_outputs: Model predictions
        all_targets: Ground truth annotations
        index_to_labels: Mapping from class indices to label names
    
    Returns:
        List of dictionaries containing formatted metrics
    """
    results = []

    # Calculate precision, recall, f1 score
    precision, recall, f1_score = calculate_detection_metrics(all_outputs, all_targets, len(index_to_labels))

    # Calculate mAP metrics
    mAP, mAP_50, mAP_75, mAP_50_95, mAP_90 = calculate_mAP_metrics(all_outputs, all_targets, len(index_to_labels))

    # Add overall metrics
    results.extend([
        {"category": "all", "splitType": split, "metricName": "precision", "metricValue": float(precision.mean().item())},
        {"category": "all", "splitType": split, "metricName": "recall", "metricValue": float(recall.mean().item())},
        {"category": "all", "splitType": split, "metricName": "f1_score", "metricValue": float(f1_score.mean().item())},
        {"category": "all", "splitType": split, "metricName": "mAP", "metricValue": float(mAP.mean().item())},
        {"category": "all", "splitType": split, "metricName": "mAP@50", "metricValue": float(mAP_50.mean().item())},
        {"category": "all", "splitType": split, "metricName": "mAP@75", "metricValue": float(mAP_75.mean().item())},
        {"category": "all", "splitType": split, "metricName": "mAP@50-95", "metricValue": float(mAP_50_95.mean().item())},
        {"category": "all", "splitType": split, "metricName": "mAP@90", "metricValue": float(mAP_90.mean().item())}
    ])

    # Add per-class metrics
    metrics_per_class = {
        "precision": precision,
        "recall": recall,
        "f1_score": f1_score,
        "AP": mAP,
        "AP@50": mAP_50,
        "AP@75": mAP_75,
        "AP@50-95": mAP_50_95,
        "AP@90": mAP_90
    }
    for i in range(len(index_to_labels)):
        for metric_name, metric_value in metrics_per_class.items():
            results.append({
                "category": index_to_labels[str(i)],
                "splitType": split,
                "metricName": metric_name,
                "metricValue": float(metric_value[i].item())
            })
    print('results from get evaluation results', results)
    return results

def calculate_mAP_metrics(outputs, targets, num_classes):
    mAP = torch.zeros(num_classes)
    mAP_50 = torch.zeros(num_classes)
    mAP_75 = torch.zeros(num_classes)
    mAP_50_95 = torch.zeros(num_classes)  # For mAP at 0.5 to 0.95
    mAP_90 = torch.zeros(num_classes)  # For mAP at 0.9

    # IoU thresholds for standard mAP calculation
    iou_thresholds = torch.linspace(0.5, 0.95, 10)

    for label in range(0, num_classes):  
        all_predictions, all_targets = collect_predictions_and_targets(outputs, targets, label)

        # Calculate mAP@50-95 (average over IoU thresholds)
        ap_sum_50_95 = sum(calculate_ap(all_predictions, all_targets, iou_threshold) for iou_threshold in iou_thresholds)
        
        mAP_50_95[label] = ap_sum_50_95 / len(iou_thresholds)  # mAP@50-95 (average over all thresholds)
        
        # Calculate mAP at specific IoU thresholds
        mAP_50[label] = calculate_ap(all_predictions, all_targets, iou_threshold=0.5)
        mAP_75[label] = calculate_ap(all_predictions, all_targets, iou_threshold=0.75)
        mAP_90[label] = calculate_ap(all_predictions, all_targets, iou_threshold=0.9)

        # Standard mAP (average over all IoU thresholds)
        mAP[label] = ap_sum_50_95 / len(iou_thresholds)  # You can also average over IoU thresholds here

    return mAP, mAP_50, mAP_75, mAP_50_95, mAP_90

def collect_predictions_and_targets(outputs, targets, label):
    all_predictions = []
    all_targets = []
    
    # Collect predictions and targets for this class
    for output, target in zip(outputs, targets):
        pred_boxes = output['boxes'][output['labels'] == label]
        pred_scores = output['scores'][output['labels'] == label]
        target_boxes = target['boxes'][target['labels'] == label]
        
        all_predictions.append((pred_boxes, pred_scores))
        all_targets.append(target_boxes)
    
    return all_predictions, all_targets

def calculate_ap(predictions, targets, iou_threshold):
    """
    Calculate Average Precision for a single class at a specific IoU threshold
    """
    # Initialize variables
    total_tp = 0
    total_fp = 0
    total_gt = sum(len(t) for t in targets)
    
    if total_gt == 0:
        return 0.0

    # Collect all predictions with their scores
    all_predictions = [(box, score) for pred_boxes, pred_scores in predictions for box, score in zip(pred_boxes, pred_scores)]
    
    # Sort predictions by confidence score
    all_predictions.sort(key=lambda x: x[1], reverse=True)
    
    # Keep track of matched targets
    matched_targets = {i: [] for i in range(len(targets))}
    
    # Calculate precision and recall points
    precisions, recalls = calculate_precision_recall(all_predictions, targets, matched_targets, iou_threshold, total_tp, total_fp, total_gt)
    
    # Calculate area under precision-recall curve
    if not precisions:
        return 0.0
        
    # Convert to numpy for easier computation
    precisions = torch.tensor(precisions)
    recalls = torch.tensor(recalls)
    
    # Interpolate precision values
    for i in range(len(precisions)-1, 0, -1):
        precisions[i-1] = max(precisions[i-1], precisions[i])
    
    # Compute AP using interpolated precision
    ap = sum(precisions[i] * (recalls[i] - recalls[i-1]) if i != 0 else precisions[i] * recalls[i] for i in range(len(precisions)))
            
    return ap

def calculate_precision_recall(all_predictions, targets, matched_targets, iou_threshold, total_tp, total_fp, total_gt):
    precisions = []
    recalls = []
    
    for i, (pred_box, _) in enumerate(all_predictions):
        # Find best matching ground truth box
        max_iou, best_match, best_target_idx = find_best_match(pred_box, targets, matched_targets, iou_threshold)
        
        if best_match is not None:
            matched_targets[best_target_idx].append(best_match)
            total_tp += 1
        else:
            total_fp += 1
            
        precision = total_tp / (total_tp + total_fp)
        recall = total_tp / total_gt
        
        precisions.append(precision)
        recalls.append(recall)
    
    return precisions, recalls


def find_best_match(pred_box, targets, matched_targets, iou_threshold):
    max_iou = iou_threshold
    best_match = None
    best_target_idx = None
    
    for target_idx, target_boxes in enumerate(targets):
        if len(target_boxes) == 0:
            continue
            
        # Skip already matched targets
        unmatched_indices = [i for i in range(len(target_boxes)) if i not in matched_targets[target_idx]]
        if not unmatched_indices:
            continue
            
        target_boxes_unmatched = target_boxes[unmatched_indices]
        ious = torchvision.ops.box_iou(pred_box.unsqueeze(0), target_boxes_unmatched)
        max_iou_for_target, max_idx = ious.max(dim=1)
        
        if max_iou_for_target > max_iou:
            max_iou = max_iou_for_target
            best_match = unmatched_indices[max_idx]
            best_target_idx = target_idx
    
    return max_iou, best_match, best_target_idx

def calculate_detection_metrics(outputs, targets, num_classes):
    all_true_positives = torch.zeros(num_classes)
    all_false_positives = torch.zeros(num_classes)
    all_false_negatives = torch.zeros(num_classes)

    for output, target in zip(outputs, targets):
        for label in range(0, num_classes):  # Skip background class (index 0)
            pred_boxes = output['boxes'][output['labels'] == label]
            target_boxes = target['boxes'][target['labels'] == label]
            if len(target_boxes) > 0:
                if len(pred_boxes) == 0:
                    all_false_negatives[label] += len(target_boxes)
                else:
                    iou = torchvision.ops.box_iou(pred_boxes, target_boxes)
                    matched_targets = (iou.max(dim=0)[0] >= 0.5).sum().item()
                    all_false_negatives[label] += len(target_boxes) - matched_targets
                    all_true_positives[label] += matched_targets
                    all_false_positives[label] += len(pred_boxes) - matched_targets

    all_precision = all_true_positives / (all_true_positives + all_false_positives + 1e-6)
    all_recall = all_true_positives / (all_true_positives + all_false_negatives + 1e-6)
    all_f1_score = 2 * all_precision * all_recall / (all_precision + all_recall + 1e-6)

    return all_precision, all_recall, all_f1_score


def get_classification_evaluation_results(split_type, outputs, targets, index_to_labels):
    predictions = torch.argmax(outputs, dim=1)
    results = []

    # Calculate basic accuracy metrics
    acc1 = accuracy(outputs, targets, topk=(1,))[0]
    acc5 = accuracy(outputs, targets, topk=(5,))[0] if len(index_to_labels) >= 5 else torch.tensor([1])

    # Calculate macro and micro metrics
    predictions_cpu = predictions.cpu()
    targets_cpu = targets.cpu()
    
    macro_metrics = {
        'precision': precision_score(predictions_cpu, targets_cpu, average="macro"),
        'recall': recall_score(predictions_cpu, targets_cpu, average="macro"), 
        'f1_score': f1_score(predictions_cpu, targets_cpu, average="macro")
    }
    
    micro_metrics = {
        'precision': precision_score(predictions_cpu, targets_cpu, average="micro"),
        'recall': recall_score(predictions_cpu, targets_cpu, average="micro"),
        'f1_score': f1_score(predictions_cpu, targets_cpu, average="micro")
    }

    weighted_metrics = {
        'precision': precision_score(predictions_cpu, targets_cpu, average="weighted"),
        'recall': recall_score(predictions_cpu, targets_cpu, average="weighted"),
        'f1_score': f1_score(predictions_cpu, targets_cpu, average="weighted")
    }
    # Calculate additional metrics
    additional_metrics = {
        'acc@1': acc1.item(),
        'acc@5': acc5.item(),
        'MCC': calculate_mcc(predictions, targets),
        'AUC-ROC': calculate_auc_roc(outputs, targets, len(index_to_labels)),
        'AUC-PR': calculate_auc_pr(outputs, targets, len(index_to_labels)),
        "Cohen's Kappa": calculate_cohen_kappa(predictions, targets),
        'log_loss': calculate_log_loss(outputs, targets),
        'specificity': specificity_all(outputs, targets),


        'micro_precision': micro_metrics['precision'],
        'micro_recall': micro_metrics['recall'],
        'micro_f1_score': micro_metrics['f1_score'],
        'macro_precision': macro_metrics['precision'],
        'macro_recall': macro_metrics['recall'],
        'macro_f1_score': macro_metrics['f1_score'],
        'weighted_precision': weighted_metrics['precision'],
        'weighted_recall': weighted_metrics['recall'],
        'weighted_f1_score': weighted_metrics['f1_score']
    }

    # Add all metrics to results
    for metric_name, value in additional_metrics.items():
        results.append({
            "category": "all",
            "splitType": split_type,
            "metricName": metric_name,
            "metricValue": float(value)
        })

    metrics_per_class = {
        'precision': precision,
        'f1_score': f1_score_per_class,
        'recall': recall,
        'specificity': specificity,
        'acc@1': accuracy_per_class
    }

    for metric_name, metric_func in metrics_per_class.items():
        for name, value in metric_func(outputs, targets).items():
            results.append({
                "category": index_to_labels[str(name)],
                "splitType": split_type,
                "metricName": metric_name,
                "metricValue": float(value)
            })

    return results


def calculate_metrics(output, target):
    """
    Calculate true positives, true negatives, false positives, and false negatives for a multi-class classification.
    """
    _, pred = output.max(1)
    pred = pred.cpu()

    true_positives = torch.zeros(output.size(1))
    true_negatives = torch.zeros(output.size(1))
    false_positives = torch.zeros(output.size(1))
    false_negatives = torch.zeros(output.size(1))

    for i in range(len(target)):
        pred_class = pred[i]
        true_class = target[i]
        for class_label in range(output.size(1)):
            if pred_class == class_label and true_class == class_label:
                true_positives[class_label] += 1
            elif pred_class == class_label and true_class != class_label:
                false_positives[class_label] += 1
            elif pred_class != class_label and true_class == class_label:
                false_negatives[class_label] += 1
            else:
                true_negatives[class_label] += 1

    return true_positives, true_negatives, false_positives, false_negatives


def accuracy_per_class(output, target):
    # Calculate TP, TN, FP, FN
    tp, tn, fp, fn = calculate_metrics(output, target)

    # Calculate accuracy for each class
    accuracy_per_class = {}
    for class_label in range(output.size(1)):
        tp_class = tp[class_label].item()
        tn_class = tn[class_label].item()
        fp_class = fp[class_label].item()
        fn_class = fn[class_label].item()
        if tp_class + tn_class + fp_class + fn_class == 0:
            accuracy = 0.0
        else:
            accuracy = (tp_class + tn_class) / (
                tp_class + tn_class + fp_class + fn_class
            )
        accuracy_per_class[class_label] = accuracy

    # Returns a dictionary where keys are class labels and values are the accuracy scores for each class.
    return accuracy_per_class


def specificity_all(output, target):
    # Calculate TN and FP for all classes
    _, tn, fp, _ = calculate_metrics(output, target)

    # Calculate overall specificity
    total_tn = tn.sum().item()
    total_fp = fp.sum().item()
    specificity = total_tn / max((total_tn + total_fp), 1e-10)

    return specificity


def accuracy(output, target, topk=(1,)):
    """Computes the accuracy over the k top predictions for the specified values of k"""
    with torch.no_grad():
        maxk = max(topk)
        batch_size = target.size(0)

        _, pred = output.topk(maxk, 1, True, True)
        pred = pred.t()
        correct = pred.eq(target.view(1, -1).expand_as(pred))

        res = []
        for k in topk:
            correct_k = correct[:k].reshape(-1).float().sum(0, keepdim=True)
            res.append(correct_k.mul_(1.0 / batch_size))

        # Returns accuracy in percentage for each value of k
        return res


def precision(output, target):
    # Calculate TP, TN, FP, FN
    tp, _, fp, _ = calculate_metrics(output, target)

    # Calculate precision for all classes
    precision_per_class = {}
    for class_label in range(output.size(1)):
        tp_class = tp[class_label].item()
        fp_class = fp[class_label].item()
        if tp_class + fp_class == 0:
            precision = 0.0
        else:
            precision = tp_class / (tp_class + fp_class)
        precision_per_class[class_label] = precision

    # Returns a dictionary where keys are class labels and values are the precision scores for each class.
    return precision_per_class


def recall(output, target):
    # Calculate TP, TN, FP, FN
    tp, _, _, fn = calculate_metrics(output, target)

    # Calculate recall for all classes
    recall_per_class = {}
    for class_label in range(output.size(1)):
        tp_class = tp[class_label].item()
        fn_class = fn[class_label].item()
        if tp_class + fn_class == 0:
            recall = 0.0
        else:
            recall = tp_class / (tp_class + fn_class)
        recall_per_class[class_label] = recall

    # Returns a dictionary where keys are class labels and values are the recall scores for each class.
    return recall_per_class


def f1_score_per_class(output, target):
    # Calculate precision and recall for all classes
    precision_per_class = precision(output, target)
    recall_per_class = recall(output, target)

    # Calculate F1 score for all classes
    f1_score_per_class = {}
    for class_label in range(output.size(1)):
        precision_class = precision_per_class[class_label]
        recall_class = recall_per_class[class_label]
        if precision_class + recall_class == 0:
            f1_score = 0.0
        else:
            f1_score = (
                2 * (precision_class * recall_class) / (precision_class + recall_class)
            )
        f1_score_per_class[class_label] = f1_score

    # Returns a dictionary where keys are class labels and values are the f1 scores for each class.
    return f1_score_per_class


def specificity(output, target):
    # Calculate TN and FP for all classes
    _, tn, fp, _ = calculate_metrics(output, target)

    # Calculate specificity for all classes
    specificity_per_class = {}
    for class_label in range(output.size(1)):
        tn_class = tn[class_label].item()
        fp_class = fp[class_label].item()
        if tn_class + fp_class == 0:
            specificity = 0.0
        else:
            specificity = tn_class / (tn_class + fp_class)
        specificity_per_class[class_label] = specificity

    # Returns a dictionary where keys are class labels and values are the specificity scores for each class.
    return specificity_per_class


# confusion metric for each class
def confusion_matrix_per_class(output, target):
    # Calculate TP, TN, FP, FN
    tp, tn, fp, fn = calculate_metrics(output, target)

    # Calculate the confusion matrix
    confusion_matrix_per_class = {}
    for class_label in range(output.size(1)):
        tp_class = tp[class_label].item()
        tn_class = tn[class_label].item()
        fp_class = fp[class_label].item()
        fn_class = fn[class_label].item()
        confusion_matrix_per_class[class_label] = [
            [tp_class, fp_class],
            [fn_class, tn_class],
        ]

    # Returns a dictionary where keys are class labels and values are confusion matrices for each class. Each confusion matrix is represented as a list: [[TP, FP], [FN, TN]].
    return confusion_matrix_per_class


# confusion metric for all classes
def confusion_matrix(output, target):
    num_classes = output.size(1)

    # Initialize the confusion matrix
    confusion_matrix_overall = torch.zeros(
        (num_classes, num_classes), dtype=torch.int64
    )
    _, predicted_classes = output.max(1)

    for i in range(target.size(0)):
        predicted_class = predicted_classes[i]
        true_class = target[i]
        confusion_matrix_overall[true_class][predicted_class] += 1

    # Returns the overall confusion matrix as a tensor, where rows correspond to true classes and columns correspond to predicted classes.
    return confusion_matrix_overall


def calculate_mcc(predictions, targets):
    return matthews_corrcoef(targets.cpu(), predictions.cpu())


def calculate_auc_roc(outputs, targets, num_classes):
    # Binarize the output and target for multi-class classification
    targets_binarized = label_binarize(targets.cpu(), classes=range(num_classes))
    # If outputs are logits, convert to probabilities
    probabilities = torch.nn.functional.softmax(outputs, dim=1).cpu().numpy()

    auc_roc = roc_auc_score(targets_binarized, probabilities, average='macro')
    return auc_roc


def calculate_auc_pr(outputs, targets, num_classes):
    # Binarize the output and target for multi-class classification
    targets_binarized = label_binarize(targets.cpu(), classes=range(num_classes))
    # If outputs are logits, convert to probabilities
    probabilities = torch.nn.functional.softmax(outputs, dim=1).cpu().numpy()

    auc_pr = average_precision_score(targets_binarized, probabilities, average='macro')
    return auc_pr

def calculate_cohen_kappa(predictions, targets):
    return cohen_kappa_score(targets.cpu(), predictions.cpu())

def calculate_log_loss(outputs, targets):
    # If outputs are logits, convert to probabilities
    probabilities = torch.nn.functional.softmax(outputs, dim=1).cpu().numpy()
    targets = targets.cpu().numpy()
    
    # Calculate Log Loss
    return log_loss(targets, probabilities)
