'''
@Author:	Jiawei He(Anson)
@Date:		2023/11/29

Crypto name list class
'''


class CryptoNameList:
    """Crypto name list class
    """
    def __init__(self, name_list: list) -> None:
        """Constructor for crypto name list class

        Args:
            name_list (list): list of crypto names to be fed in

        Raises:
            TypeError
            ValueError
        """

        if not isinstance(name_list, list):
            raise TypeError("Crypto name list must be a list")
        if len(name_list) == 0:
            raise ValueError("Data fed in should not be 0")
        self.name_list = name_list

        # ------------

        # More attributes for further development beyond this project
        # self.enriched_crypto_data = {name: None for name in name_list}

    def count_crypto_names(self) -> int:
        """returns the number of crypto names in the list

        Returns:
            int: number of crypto names in the list
        """

        count = len(self.name_list)
        return count

    # ------------
    # More methods for further development beyond this project

    # def get_enriched_data(self, crypto_name: str) -> dict:
    #     # Get the enriched data from the crypto name
    #     # ...
    #     return self.enriched_crypto_data.get(crypto_name)

    # def update_enriched_data(self, crypto_name: str) -> None:
    #     # Update the enriched data from the crypto name
    #     # ...
