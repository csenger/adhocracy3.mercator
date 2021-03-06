"""Proposal resource type."""
from adhocracy_core.interfaces import IItemVersion
from adhocracy_core.interfaces import ITag
from adhocracy_core.interfaces import IItem
from adhocracy_core.resources.comment import add_commentsservice
from adhocracy_core.resources.sample_section import ISection
from adhocracy_core.resources.sample_paragraph import IParagraph
from adhocracy_core.resources import add_resource_type_to_registry
from adhocracy_core.resources.itemversion import itemversion_metadata
from adhocracy_core.resources.item import item_metadata
from adhocracy_core.resources.rate import add_ratesservice

import adhocracy_core.sheets.document
import adhocracy_core.sheets.comment


class IProposalVersion(IItemVersion):

    """Versionable item with Document propertysheet."""


proposalversion_meta = itemversion_metadata._replace(
    content_name='ProposalVersion',
    iresource=IProposalVersion,
    basic_sheets=[adhocracy_core.sheets.versions.IVersionable,
                  adhocracy_core.sheets.metadata.IMetadata,
                  ],
    extended_sheets=[adhocracy_core.sheets.document.IDocument,
                     adhocracy_core.sheets.comment.ICommentable
                     ],
    permission_add='add_proposalversion',
)


class IProposal(IItem):

    """All versions of a Proposal."""


proposal_meta = item_metadata._replace(
    content_name='Proposal',
    iresource=IProposal,
    element_types=[ITag,
                   ISection,
                   IParagraph,
                   IProposalVersion,
                   ],
    after_creation=item_metadata.after_creation + [
        add_commentsservice,
        add_ratesservice,
    ],
    item_type=IProposalVersion,
    permission_add='add_proposal',
    is_implicit_addable=True,
)


def includeme(config):
    """Add resource type to registry."""
    add_resource_type_to_registry(proposalversion_meta, config)
    add_resource_type_to_registry(proposal_meta, config)
