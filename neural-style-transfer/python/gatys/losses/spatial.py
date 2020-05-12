"""
INFO8010-1 - Deep learning
University of Liège
Academic year 2019-2020

Project : neural style transfer

Authors :
    - Maxime Meurisse
    - Adrien Schoffeniels
    - Valentin Vermeylen
"""

###########
# Imports #
###########

import torch
import torch.nn as nn


#############
# Functions #
#############

def guided(input, guidance_channels):
    """# Computes the correct Fs as described in the paper and
    returns them as an array of size R"""

    # The Fr as described in the paper
    fr = []

    for channel in guidance_channels:
        f = torch.Tensor(input.size())

        for column in range(input.size()[3]):
            f[:, column] = torch.mul(channel, input[:, column])

        fr.append(f)

    return fr


def gram_matrix(input):
    return torch.mm(input, input.t())


###########
# Classes #
###########

class ContentLoss(nn.Module):
    def __init__(self, reference):
        """
        Initializes the content loss with the reference tensor.
        Since reference is not a variable in the computation tree,
        we need to detach it in order to avoid it being taken into
        account in the backpropagation.
        """

        super(ContentLoss, self).__init__()

        self.reference = reference.detach()

    def forward(self, x):
        """
        Computes the MSE between the reference and the tensor x and
        returns the input x so as not to interfere with the forward
        pass of the model.
        """

        self.loss = functional.mse_loss(x, self.reference)

        return x


class StyleLoss(nn.Module):
    def __init__(self, reference, guidance_channels):
        """
        Initializes the style loss with the reference tensor.
        As for the content loss, the reference is detached before
        being assigned to a field.
        """

        super(StyleLoss, self).__init__()

        self.gram_reference = gram_matrix(
            guided(reference, guidance_channels)
        ).detach()

    def forward(self, x):
        """
        Computes the loss and returns the input tensor x.
        """

        a, b, c, d = x.size()

        self.loss = functional.mse_loss(
            input=gram_matrix(x),
            target=self.gram_reference
        )
        self.loss /= (2 * b ** 2 * (c * d) ** 2)

        return x