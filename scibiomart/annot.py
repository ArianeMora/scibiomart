###############################################################################
#                                                                             #
#    This program is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU General Public License as published by     #
#    the Free Software Foundation, either version 3 of the License, or        #
#    (at your option) any later version.                                      #
#                                                                             #
#    This program is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#    GNU General Public License for more details.                             #
#                                                                             #
#    You should have received a copy of the GNU General Public License        #
#    along with this program. If not, see <http://www.gnu.org/licenses/>.     #
#                                                                             #
###############################################################################

"""
Adds annotation to a dataframe.
"""
import pandas as pd

from scibiomart import SciBiomartApi


class Annot(SciBiomartApi):

    def __init__(self):
        super().__init__()

    def annot(self, df: pd.DataFrame, merge_ids: list, annotation_df=None, keep_na=False):
        """ Adds annotation information to a dataframe. """
        if self.df is None and annotation_df is None:
            self.u.err_p(['Annot error: you need to pass a dataframe or generate annotation dataframe '
                          'using scibiomart. See get_mouse_default and get_human_default for examples.'])
            return

        # Otherwise we can continue
        # We can do a merge on the index's (an inner merge if we don't have keep na)
        df.set_index(merge_ids[0])
        annotation_df.set_index(merge_ids[1])
        if not keep_na:
            merged_df = df.join(annotation_df, how='inner')
            return merged_df
        else:
            return df.join(annotation_df, how='outer')
