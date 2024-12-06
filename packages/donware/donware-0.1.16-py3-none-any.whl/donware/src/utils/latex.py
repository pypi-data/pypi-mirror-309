#!/Users/donyin/miniconda3/bin/python
# \usepackage{graphicx}
# \usepackage{tabularray}

import re
from rich import print
from pathlib import Path
from pyperclip import copy
from itertools import product


class Equation:
    def __init__(self, equation: str | list[str]):
        if isinstance(equation, str):
            self.equation = equation
        elif isinstance(equation, list):
            self.equation = "\\begin{aligned}\n"
            for i, line in enumerate(equation):
                self.equation += f"    &{line}"
                if i < len(equation) - 1:
                    self.equation += "\\\\\n"
                else:
                    self.equation += "\n"
            self.equation += "\\end{aligned}"

    def __str__(self):
        return self.equation


def create_latex_table(
    data: list[dict],
    caption: str = "Models",
    label: str = "tab:models",
    font_size: float = 5.5,
    display_option: str = "h",
    first_col_width: float = 0.1,
) -> None:
    # --- first of all assert that the items in data have the same keys ---
    for i in range(1, len(data)):
        assert data[i].keys() == data[0].keys(), f"Keys in data at index {i} do not match keys in data at index 0"

    # --- create the LaTeX table ---
    lines = []
    lines.append(f"\\begin{{table}}[{display_option}]")
    lines.append("\t\\centering")
    lines.append("\t\\setlength{\\tabcolsep}{4pt}")
    lines.append("\t\\begin{tblr}{")
    lines.append("\t\twidth=\\textwidth,")

    # colspec = "|" + "|".join(["X[1]"] + ["X[2]" for _ in range(len(data))]) + "|"
    # lines.append(f"\t\tcolspec={{{colspec}}},")
    colspec = f"|X[{first_col_width}]|" + "|".join([f"X[{(1-first_col_width)/len(data):.2f}]" for _ in range(len(data))]) + "|"
    lines.append(f"\t\tcolspec={{{colspec}}},")
    lines.append(f"\t\trow{{1-Z}}={{font={{\\fontsize{{{font_size}pt}}{{6.6pt}}\\selectfont}}, m}},")
    lines.append(f"\t\tcell{{1-Z}}{{1-{len(data)+1}}}={{c, m}},")
    lines.append("\t\thlines")
    lines.append("\t}")

    # Add header row
    first_key = next(iter(data[0]))
    header = f"\t\\textbf{{{first_key}}} & " + " & ".join([f"\\textbf{{{item[first_key]}}}" for item in data])
    lines.append(header + " \\\\")

    for key in data[0].keys():
        if key == first_key:
            continue  # Skip Model Name as it's used in the header

        if isinstance(data[0][key], Equation):
            item_str = f"\t\\textbf{{{key}}}"
            for item in data:
                item_str += f" & ${item[key].equation}$"
            lines.append(item_str + " \\\\")

        elif isinstance(data[0][key], Path):
            item_str = f"\t\\SetCell[r=2]{{m}} \\textbf{{{key}}}"
            for item in data:
                item_str += (
                    f" & \\SetCell[r=2]{{m}} \\includegraphics[width=0.9\\linewidth,height=2cm,keepaspectratio]{{{item[key]}}}"
                )
            lines.append(item_str + " \\\\")
            lines.append("\t" + " & " * len(data) + " \\\\")  # Empty row for image spacing

        else:
            item_str = f"\t\\textbf{{{key}}}"
            for item in data:
                item_str += f" & {item[key]}"
            lines.append(item_str + " \\\\")

    lines.append("\t\\end{tblr}")
    lines.append(f"\t\\caption{{{caption}}}")
    lines.append(f"\t\\label{{{label}}}")
    lines.append("\\end{table}")

    copy("\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    # --- multi-line equation example ---
    data_table_framework = [
        {
            "Layer": "Convolutional",
            "Formula": Equation("f_{\\text{conv}}"),
            "Output": Path("images/conv.png"),
        },
        {
            "Layer": "Max-Pooling",
            "Formula": Equation("f_{\\text{max}}"),
            "Output": Path("images/max.png"),
        },
        {
            "Layer": "Flexible",
            "Formula": Equation(
                [
                    "\\text{Logits:} && \\text{logits} = T - f_{\\text{max}}",
                    "\\text{Mask:} && \\text{mask} = \\sigma(\\text{logits} \cdot s)",
                    "\\text{Output:} && \\text{mask} \\cdot f_{\\text{conv}} + \overline{\\text{mask}} \cdot f_{\\text{max}}",
                ]
            ),
            "Output": Path("images/mlp.png"),
        },
    ]

    # --- measures table ---
    data_table_measures = [
        {
            "Measure": "Convolutional Ratio",
            "Description": "The ratio of convolutional units within a layer",
            "Formula": Equation("\\frac{\\text{Number of Convolutional Units}}{\\text{Total Number of Units}}"),
            "Output": Path("images/measure-conv-ratio.png"),
        },
        {
            "Measure": "Operation Homogeneity",
            "Description": "The degree to which one operation is weighted more significantly than another. Higher homogeneity indicates one operation dominates, while lower homogeneity (heterogeneity) suggests more balanced weighting between the two operations.",
            "Formula": Equation("\\frac{1}{n} \\sum_{i=1}^n (|\\text{mask}_i - 0.5| \\cdot 2)"),
            "Output": Path("images/measure-homogeneity.png"),
        },
    ]

    # --- logits table ---
    data_table_logits = [
        {
            "Mechanism": "Trainable Thresholds",
            "Equation": Equation("\\text{logits} = T - f_{\\text{max}}"),
            "Description": Equation(
                [
                    "T = \\text{learned parameters}",
                    "\\text{adjusted during training}",
                ]
            ),
        },
        {
            "Mechanism": "Spatial Attention Blocks",
            "Equation": Equation(
                [
                    "\\text{Block} = \\text{BatchNorm}(\\text{ReLU}(\\text{Conv}(\\text{input})))",
                    "\\text{logits} = \\text{Block}_{}^{(2)}(\\text{input})",
                ]
            ),
            "Description": Equation(
                [
                    "\\text{Block}^{(i)} = \\text{applied i times to input tensor}",
                ]
            ),
        },
    ]

    # --- mask table ---
    data_table_mask_1 = [
        {
            "Activation Function": "Straight-Through Estimator",
            "Forward": Equation(
                [
                    "\\text{mask} = \\begin{cases} 1 & \\text{if } \\sigma(\\text{logits}) > 0.5 \\\\ 0 & \\text{otherwise} \\end{cases}",
                ]
            ),
            "Backward": Equation(
                [
                    "\\text{grad}_\\text{logits} = \\text{grad}_\\text{output} \\cdot \\sigma(\\text{logits})(1 - \\sigma(\\text{logits}))",
                ]
            ),
            "Description": Equation(
                [
                    "\\text{grad}_\\text{logits}: \\text{gradient w.r.t. logits}",
                    "\\text{grad}_\\text{output}: \\text{gradient from next layer}",
                ]
            ),
            "Dipiction": Path("images/manim/__main/mask-step-function.png"),
        },
        {
            "Activation Function": "Stochastic Rounding",
            "Forward": Equation(
                [
                    "logits' = \\sigma(logits)",
                    "mask =",
                    "\\Delta \\cdot \\left\\{\\begin{array}{l} \\left\\lfloor \\frac{logits'}{\\Delta} \\right\\rfloor + 1 \\quad \\text{if } p \\leq logits' - \\left\\lfloor \\frac{logits'}{\\Delta} \\right\\rfloor \\Delta \\\\ \\left\\lfloor \\frac{logits'}{\\Delta} \\right\\rfloor \\quad \\text{otherwise} \\end{array}\\right.",
                ]
            ),
            "Backward": Equation(
                [
                    "\\text{grad}_\\text{logits} = \\text{grad}_\\text{output} \\cdot \\sigma(\\text{logits})(1 - \\sigma(\\text{logits}))",
                ]
            ),
            "Description": Equation(
                [
                    "logits: \\text{original continuous logits value}",
                    "logits': \\text{logits processed via a sigmoid function}",
                    "\\Delta: \\text{quantization step size (set to 1 in this case)}",
                    "p: \\text{uniformly distributed random variable in the range [0, 1]}",
                    "\\left\\lfloor \\cdot \\right\\rfloor: \\text{floor function}",
                    "logits' - \\left\\lfloor \\frac{logits'}{\\Delta} \\right\\rfloor \\Delta: \\text{the residual part of logits'}",
                ]
            ),
            "Dipiction": Path("images/manim/__main/mask-sr.png"),
        },
    ]

    # --- mask table 2 ---
    data_table_mask_2 = [
        {
            "Activation Function": "Hard Sigmoid",
            "Equation": Equation("\\text{mask} = \\text{clamp}(\\frac{\\text{logits} + 1}{2}, 0, 1)"),
            "Description": Equation("\\text{piecewise linear approximation of sigmoid}"),
            "Dipiction": Path("images/manim/__main/mask-hard-sigmoid.png"),
        },
        {
            "Activation Function": "Sigmoid with Scaling Factor",
            "Equation": Equation("\\text{mask} = \\sigma(\\text{logits} \\times 50)"),
            "Description": Equation("\\sigma(x) = \\frac{1}{1 + e^{-x}}"),
            "Dipiction": Path("images/manim/__main/mask-scaled-sigmoid.png"),
        },
    ]

    # ---- table that compares cmp and conv / max pooling ----
    data_table_cmp_vs_conv = [
        {
            "Layer": "Convolutional",
            "Formula": Equation("f_{\\text{conv}}"),
            "Output": Path("images/conv.png"),
        },
        {
            "Layer": "Max-Pooling",
            "Formula": Equation("f_{\\text{max}}"),
            "Output": Path("images/max.png"),
        },
        {
            "Layer": "Channel-wise Max-Pooling",
            "Formula": Equation(
                [
                    "f_{\\text{flex}}[i, j, k] =",
                    "\\max\\left( f_{\\text{conv}}[i, j, k], f_{\\text{max}}[i, j, k] \\right)",
                ]
            ),
            "Output": Path("images/cmp.png"),
        },
    ]

    # ---- attacks table ----
    data_table_attacks = [
        {
            "Attack": "FGSM",
            "Nature": "White-box",
            "Description": "Fast Gradient Sign Method: Perturbs input in direction of gradient of loss w.r.t. input",
            "Epsilon Conversion": Equation("\\text{eps} = \\epsilon"),
            "Epsilon Range": Equation("\\epsilon \\in [0, 0.64]"),
        },
        {
            "Attack": "PGD",
            "Nature": "White-box",
            "Description": "Projected Gradient Descent: Iterative version of FGSM with random initialization",
            "Epsilon Conversion": Equation(["\\text{eps} = \\epsilon", "\\text{alpha} = \\epsilon / 4", "\\text{steps} = 20"]),
            "Epsilon Range": Equation("\\epsilon \\in [0, 23/255]"),
        },
        {
            "Attack": "SPGD",
            "Nature": "White-box",
            "Description": "Strong PGD: A stronger, more aggressive variant of PGD using higher epsilon values",
            "Epsilon Conversion": Equation(["\\text{eps} = \\epsilon", "\\text{alpha} = \\epsilon / 4", "\\text{steps} = 20"]),
            "Epsilon Range": Equation("\\epsilon \\in [0, 0.5]"),
        },
        {
            "Attack": "Jitter",
            "Nature": "White-box",
            "Description": "Adds random noise to input, then clips to maintain similarity to original",
            "Epsilon Conversion": Equation(
                ["\\text{eps} = \\epsilon", "\\text{alpha} = \\epsilon / 4", "\\text{steps} = 20", "\\text{scale} = 10"]
            ),
            "Epsilon Range": Equation("\\epsilon \\in [0, 0.3]"),
        },
        {
            "Attack": "OnePixel",
            "Nature": "Black-box",
            "Description": "Modifies a single pixel to cause misclassification",
            "Epsilon Conversion": Equation(
                [
                    "\\text{pixels} = \\max(1, \\lfloor\\epsilon\\rfloor)",
                    "\\text{steps} = \\lfloor2\\epsilon\\rfloor",
                    "\\text{popsize} = \\lfloor\\epsilon\\rfloor",
                    "\\text{inf\\_batch} = 128",
                ]
            ),
            "Epsilon Range": Equation("\\epsilon \\in [1, 42]"),
        },
        {
            "Attack": "SPSA",
            "Nature": "Black-box",
            "Description": "Simultaneous Perturbation Stochastic Approximation: Estimates gradient using random perturbations",
            "Epsilon Conversion": Equation(
                [
                    "\\text{eps} = \\epsilon",
                    "\\text{delta} = 0.01",
                    "\\text{lr} = 0.01",
                    "\\text{nb\\_iter} = \\lfloor40\\epsilon\\rfloor",
                    "\\text{nb\\_sample} = 128",
                    "\\text{max\\_batch\\_size} = 16",
                ]
            ),
            "Epsilon Range": Equation("\\epsilon \\in [0, 0.21]"),
        },
    ]

    # ---- attack examples table ----
    data_table_attacks_examples = [
        {
            "Attack": "FGSM",
            "CIFAR-10": Path("images/adversarial-examples/VGG6-CIFAR-10-trained/FGSM.png"),
            "ImageNet-100": Path("images/adversarial-examples/VGG16-ImageNet-100-untrained/FGSM.png"),
        },
        {
            "Attack": "PGD",
            "CIFAR-10": Path("images/adversarial-examples/VGG6-CIFAR-10-trained/PGD.png"),
            "ImageNet-100": Path("images/adversarial-examples/VGG16-ImageNet-100-untrained/PGD.png"),
        },
        {
            "Attack": "SPGD",
            "CIFAR-10": Path("images/adversarial-examples/VGG6-CIFAR-10-trained/SPGD.png"),
            "ImageNet-100": Path("images/adversarial-examples/VGG16-ImageNet-100-untrained/SPGD.png"),
        },
        {
            "Attack": "Jitter",
            "CIFAR-10": Path("images/adversarial-examples/VGG6-CIFAR-10-trained/Jitter.png"),
            "ImageNet-100": Path("images/adversarial-examples/VGG16-ImageNet-100-untrained/Jitter.png"),
        },
        {
            "Attack": "OnePixel",
            "CIFAR-10": Path("images/adversarial-examples/VGG6-CIFAR-10-trained/OnePixel.png"),
            "ImageNet-100": Path("images/adversarial-examples/VGG16-ImageNet-100-untrained/OnePixel.png"),
        },
        {
            "Attack": "SPSA",
            "CIFAR-10": Path("images/adversarial-examples/VGG6-CIFAR-10-trained/SPSA.png"),
            "ImageNet-100": Path("images/adversarial-examples/VGG16-ImageNet-100-untrained/SPSA.png"),
        },
    ]

    # Invert the attack examples dictionary
    inverted_data_table_attacks_examples = []
    all_columns = list(data_table_attacks_examples[0].keys())
    for column in all_columns:
        new_row = {"Dataset/Attack": column}
        for original_row in data_table_attacks_examples:
            attack_name = original_row["Attack"]
            new_row[attack_name] = original_row.get(column, "N/A")
        inverted_data_table_attacks_examples.append(new_row)
    data_table_attacks_examples = inverted_data_table_attacks_examples

    # --- final results table ---
    datasets = ["CIFAR-10", "ImageNet-100"]
    logits_mechanisms = ["Threshold", "SAB"]
    mask_mechanisms = ["Scaled Sigmoid", "STE", "SR", "Hard Sigmoid"]

    data_table_final_results = []

    # Generate combinations
    for dataset, logits, mask in product(datasets, logits_mechanisms, mask_mechanisms):
        data_table_final_results.append(
            {
                "Dataset": dataset,
                "Logits Mechanism": logits,
                "Mask Mechanism": mask,
                "Training Accuracy": "TODO",
                "Training Loss": "TODO",
                "Validation Accuracy": "TODO",
                "Validation Loss": "TODO",
            }
        )

    # Add the two CMP rows
    for dataset in datasets:
        data_table_final_results.append(
            {
                "Dataset": dataset,
                "Logits Mechanism": "CMP",
                "Mask Mechanism": "CMP",
                "Training Accuracy": f"TODO",
                "Training Loss": f"TODO",
                "Validation Accuracy": f"TODO",
                "Validation Loss": f"TODO",
            }
        )

    # Invert rows and columns for data_table_final_results
    inverted_data_table_final_results = []
    all_columns = list(data_table_final_results[0].keys())
    for column in all_columns:
        new_row = {"Metric": column}
        for i, original_row in enumerate(data_table_final_results):
            new_row[f"Config {i+1}"] = original_row.get(column, "N/A")
        inverted_data_table_final_results.append(new_row)
    data_table_final_results = inverted_data_table_final_results

    # Create training curve data table
    data_table_training_curves = [
        {
            "Metric": "Accuracy",
            "CIFAR-10": Path("images/cifar10_accuracy_curve.png"),
            "ImageNet-100": Path("images/imagenet100_accuracy_curve.png"),
        },
        {
            "Metric": "Loss",
            "CIFAR-10": Path("images/cifar10_loss_curve.png"),
            "ImageNet-100": Path("images/imagenet100_loss_curve.png"),
        },
    ]

    # ---- create spectrum data table ----
    {
        "000011": "VGG6",
        "000001": "Flex: Threshold + Scaled Sigmoid",
        "000002": "Flex: Threshold + Hard Sigmoid",
        "000003": "Flex: Threshold + STE",
        "000004": "Flex: Threshold + SR",
        "000006": "Flex: SAB + Scaled Sigmoid",
        "000007": "Flex: SAB + Hard Sigmoid",
        "000008": "Flex: SAB + STE",
        "000009": "Flex: SAB + SR",
        "000010": "Flex: CMP",
    }

    logits_mechanisms = ["Threshold", "SAB"]
    mask_mechanisms = ["Scaled Sigmoid", "STE", "SR", "Hard Sigmoid"]

    data_table_spectrum = []

    data_table_spectrum.append(
        {
            "Description": "VGG6",
            "Hessian Spectrum": Path(f"images/plots/hessian/000011.png"),
            "Loss Landscape (small)": Path(f"images/plots/distance-0/000011.png"),
            "Loss Landscape (large)": Path(f"images/plots/distance-1/000011.png"),
        }
    )

    key_mapping = {
        ("Threshold", "Scaled Sigmoid"): "000001",
        ("Threshold", "Hard Sigmoid"): "000002",
        ("Threshold", "STE"): "000003",
        ("Threshold", "SR"): "000004",
        ("SAB", "Scaled Sigmoid"): "000006",
        ("SAB", "Hard Sigmoid"): "000007",
        ("SAB", "STE"): "000008",
        ("SAB", "SR"): "000009",
    }

    for logits, mask in product(logits_mechanisms, mask_mechanisms):
        key = key_mapping.get((logits, mask))
        if key:
            data_table_spectrum.append(
                {
                    "Description": f"{logits} + {mask}",
                    "Hessian Spectrum": Path(f"images/plots/hessian/{key}.png"),
                    "Loss Landscape (small)": Path(f"images/plots/distance-0/{key}.png"),
                    "Loss Landscape (large)": Path(f"images/plots/distance-1/{key}.png"),
                }
            )

    # Add CMP separately
    data_table_spectrum.append(
        {
            "Description": "Flex: CMP",
            "Hessian Spectrum": Path(f"images/plots/hessian/000010.png"),
            "Loss Landscape (small)": Path(f"images/plots/distance-0/000010.png"),
            "Loss Landscape (large)": Path(f"images/plots/distance-1/000010.png"),
        }
    )

    # Invert rows and columns for data_table_spectrum
    inverted_data_table_spectrum = []
    all_columns = list(data_table_spectrum[0].keys())
    for column in all_columns:
        new_row = {"Metric": column}
        for i, original_row in enumerate(data_table_spectrum):
            new_row[f"{i+1}"] = original_row.get(column, "N/A")
        inverted_data_table_spectrum.append(new_row)
    data_table_spectrum = inverted_data_table_spectrum

    print(data_table_spectrum)

    # ==== plotting ====
    # create_latex_table(
    #     data_table_framework,
    #     caption="\\sigma() is the sigmoid function, T is the threshold tensor adjusted during training, and s is the scaling factor (hard-coded as 50).",
    #     label="tab:layers",
    #     font_size=5.5,
    #     display_option="h",
    #     first_col_width=0.1,
    # )

    # create_latex_table(
    #     data_table_measures,
    #     caption="Both measures are taken across the entire test set.",
    #     label="tab:measures",
    #     font_size=5.5,
    #     display_option="h",
    #     first_col_width=0.1,
    # )

    # create_latex_table(
    #     data_table_logits,
    #     caption="Logits mechanisms used in the FL.",
    #     label="tab:logits_overall",
    #     font_size=5.5,
    #     display_option="h",
    #     first_col_width=0.15,
    # )

    create_latex_table(
        data_table_mask_1,
        caption="Mask computations used in the FL.",
        label="tab:mask_mechanisms_1",
        font_size=5.5,
        display_option="h",
        first_col_width=0.1,
    )

    # create_latex_table(
    #     data_table_mask_2,
    #     caption="Mask computations used in the FL.",
    #     label="tab:mask_mechanisms_2",
    #     font_size=5.5,
    #     display_option="h",
    #     first_col_width=0.1,
    # )

    # create_latex_table(
    #     data_table_cmp_vs_conv,
    #     caption="Comparison of the Flexible Layer with Convolutional and Max-Pooling Layers. The Flexible Layer combines these operations as $f_{\\text{flex}} = \\max(f_{\\text{conv}}, f_{\\text{max}})$, where each output element is selected by taking the larger value of the convolution and Max-Pooling output at the corresponding index.",
    #     label="tab:cmp_vs_conv",
    #     font_size=5.5,
    #     display_option="h",
    #     first_col_width=0.1,
    # )

    # create_latex_table(
    #     data_table_attacks,
    #     caption="Overview of the attacks used in the FL.",
    #     label="tab:attacks",
    #     font_size=5.5,
    #     display_option="h",
    #     first_col_width=0.1,
    # )

    # create_latex_table(
    #     data_table_attacks_examples,
    #     caption="Examples of the attacks used in the FL.",
    #     label="tab:attacks_examples",
    #     font_size=5.5,
    #     display_option="h",
    #     first_col_width=0.1,
    # )

    # create_latex_table(
    #     data_table_final_results,
    #     caption="Final results of various FL setups on the CIFAR-10 and ImageNet-100 datasets.",
    #     label="tab:final_results",
    #     font_size=5.5,
    #     display_option="h",
    #     first_col_width=0.1,
    # )

    # create_latex_table(
    #     data_table_training_curves,
    #     caption="Training and validation curves for CIFAR-10 and ImageNet-100 datasets.",
    #     label="tab:training_curves",
    #     font_size=5.5,
    #     display_option="h",
    #     first_col_width=0.1,
    # )

    # create_latex_table(
    #     data_table_spectrum,
    #     caption="Hessian spectrums and loss landscape for different combinations of logits and mask mechanisms. A broader spectrum indicates more eigenvalues with larger absolute values, suggesting more curvature and saddle points. This graph does not show the difference between curvatures at different scales as the probability estimate is processed by kernels.",
    #     label="tab:hessian_spectrums",
    #     font_size=5.5,
    #     display_option="h",
    #     first_col_width=0.07,
    # )
