import argparse
import os
import json

import utils
import dataset
import modules


def parse_args():
    parser = argparse.ArgumentParser(description="Train a deep learning model with specified parameters.")
    parser.add_argument("-t", "--type", type=str, required=True, help="Type is classification or regression.")
    parser.add_argument("-p", "--path", type=str, required=True, help="Path to the dataset.")
    parser.add_argument("-d", "--devices", type=int, nargs="+", default=[0], help="List of GPU device IDs to use for training.")
    parser.add_argument("-r", "--result",  type=str, required=True, help="Path to the result directory.")
    return parser.parse_args()

    
def main():
    args = parse_args()
    config_path = args.result
    configs = utils.load_config(config_path)
        
    print("Config loaded from:", os.path.join(config_path, "config.json"))
    print("--------\nconfig:\n", json.dumps(configs, indent=2))
    print("--------")
    print(f"Task type: {args.type}")
    print(f"Using devices: {args.devices}")
    print(f"Dataset path: {args.path}")
    print(f"Result path: {args.result}")
    print("--------")
    
    device = utils.setup_device(args.devices)
    dataList, dataLabel, idTmps = dataset.process_data(args.path, args.type)
    trainloader = dataset.get_dataloader(dataList, dataLabel, idTmps, batch_size=1, shuffle=True)
    model_path = utils.train_model(args.type, configs['model']['learning_rate'], trainloader, device, configs['model']['epochs'],args.result)
    
    df_attr = modules.calculate_attribution_scores(model_path, args.type, dataList, dataLabel, idTmps, args.path, args.result, device)
    utils.plot_attribution_scores(args.type, df_attr, args.result)
    
    df_attn = modules.calculate_attention_scores(model_path, trainloader, args.path, args.result, device)
    utils.plot_attention_scores(args.type, df_attn, args.path, args.result)
    
if __name__ == "__main__":
    main()