#!/usr/bin/python3
from brownie import AdvancedCollectible
from scripts.helpful_scripts import fund


def main():
    advanced_collectible = AdvancedCollectible[len(AdvancedCollectible) - 1]
    fund(advanced_collectible)
