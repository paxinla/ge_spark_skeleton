# 在 Spark(PySpark) 上使用 Great Expectation 示例

最终生成 wheel 包以安装到运行环境里，然后可由 orchestration software 调度执行。


1. 首先编辑 `PRJECT_NAME.txt` 文件，写入项目名称，名称应仅包含小写字母及数字，以字母开头。
2. 执行 `make init` 安装 Python 依赖，生成必要的目录和文件。
3. 在 `xxx_expectations/data_assets` 目录下，为每个需要检测的数据集创建一个类，继承 `dataset.py` 中的 SparkDataset 类。
4. 在 `xxx_expectations/rules` 目录下，为每个需要采用的检测规则创建一个类。可用的规则见[官网 Expectations Gallery](https://greatexpectations.io/expectations/)
5. 编辑 `xxx_expectations/mapping.py` 文件，添加每一对 (数据集, 规则) 到 `DATASET_RULE_MAP` 中。


## Requirements

本地环境必须已安装 Python (>= 3.8) 和 pip ，并设置了虚拟环境的目录。修改 Makefile 中的 VMROOT 指向虚拟环境的目录。


## Usage

+ `make init` : 在本地虚拟环境中安装 Python 依赖库。
+ `make wheel` : 生成 wheel 包。

